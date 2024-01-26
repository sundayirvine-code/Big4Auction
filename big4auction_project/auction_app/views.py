from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os
from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
stripe.api_key = STRIPE_SECRET_KEY


def get_setup_intent_page(request):
    return render(request, 'auction_app/register-card.html')

def get_publishable_key(request):
    return JsonResponse({'publicKey': STRIPE_PUBLIC_KEY})

@csrf_exempt
def create_setup_intent(request):
    customer = stripe.Customer.create()
    setup_intent = stripe.SetupIntent.create(customer=customer.id)
    return JsonResponse({
        'client_secret': setup_intent.client_secret,
        'customer': customer.id
        })

@csrf_exempt
def webhook_received(request):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.body.decode('utf-8'))

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    customer = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'setup_intent.created':
        print('🔔 A new SetupIntent was created.')
    
    if event["type"] == "setup_intent.succeeded":
        print('🔔 A SetupIntent has successfully set up a PaymentMethod for future use.')

    if event["type"]== 'payment_method.attached':
        print('🔔 A PaymentMethod has successfully been saved to a Customer.')
        # At this point, redirect to the register page and pass the ID of the Customer object. 
        # This will be associated with the internal representation of a user.

    if event["type"] == 'setup_intent.setup_failed':
        print('🔔 A SetupIntent has failed the attempt to set up a PaymentMethod.')


    return redirect('registration', customer_id=customer.id)


def registration(request, customer_id):
    if not customer_id:
        return HttpResponse("Invalid request. Missing customer_id parameter.")

    context = {'customer_id': customer_id}

    # Process form submission
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            hashed_password = make_password(form.cleaned_data['password1'])
            user = User(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=hashed_password,
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
                stripe_customer_id=customer_id
            )
            user.save()
            return redirect('login')
    else:
        # Render the form for initial GET request
        form = RegistrationForm()

    context['form'] = form
    return render(request, 'auction_app/registration.html', context)

def login_view(request):
    """
    View for handling user login.

    If the provided email and password match a user, the user is logged in.
    Redirects to the login page with an error message if authentication fails.

    Args:
        request: The HTTP request.

    Returns:
        HttpResponse: A success message or a redirection to the login page with an error.
    """
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

        if check_password(password, user.password):
            authenticated_user = user
            login(request, authenticated_user)

            # Redirect to a success page or perform other actions
            print('logged in')
            return HttpResponse('success')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    form = LoginForm()
    return render(request, 'auction_app/login.html', {'form': form})
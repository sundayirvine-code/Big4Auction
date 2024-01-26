from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm, LoginForm
from .models import User
from django.contrib import messages
import stripe
import os
import json

# Retrieve Stripe API keys from environment variables
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
stripe.api_key = STRIPE_SECRET_KEY


def get_setup_intent_page(request):
    """Render the page for setting up a payment method."""
    return render(request, 'auction_app/register-card.html')


def get_publishable_key(request):
    """Return the public key for Stripe."""
    return JsonResponse({'publicKey': STRIPE_PUBLIC_KEY})


@csrf_exempt
def create_setup_intent(request):
    """Create a SetupIntent for setting up a payment method."""
    customer = stripe.Customer.create()
    setup_intent = stripe.SetupIntent.create(customer=customer.id)
    return JsonResponse({
        'client_secret': setup_intent.client_secret,
        'customer': customer.id
    })


@csrf_exempt
def webhook_received(request):
    """Handle Stripe webhook events."""
    webhook_secret = STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.body.decode('utf-8'))
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    customer_id = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle different Stripe webhook events
    if event['type'] == 'setup_intent.created':
        print('🔔 A new SetupIntent was created.')
    elif event["type"] == "setup_intent.succeeded":
        print('🔔 A SetupIntent has successfully set up a PaymentMethod for future use.')
    elif event["type"] == 'payment_method.attached':
        print('🔔 A PaymentMethod has successfully been saved to a Customer.')
        customer_id = event['data']['object']['customer']
    elif event["type"] == 'setup_intent.setup_failed':
        print('🔔 A SetupIntent has failed the attempt to set up a PaymentMethod.')

    return redirect('registration', customer_id=customer_id)


def registration(request, customer_id):
    """Handle user registration after setting up a payment method."""
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
    """Handle user login."""
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
            return HttpResponse('success')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    form = LoginForm()
    return render(request, 'auction_app/login.html', {'form': form})

from django.shortcuts import render
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import os

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

stripe.api_key = STRIPE_SECRET_KEY

# will serve as the stripe card
def get_setup_intent_page(request):
    return render(request, 'auction_app/index.html')

def get_publishable_key(request):
    return JsonResponse({'publicKey': STRIPE_PUBLIC_KEY})

@csrf_exempt
def create_setup_intent(request):
    customer = stripe.Customer.create()
    setup_intent = stripe.SetupIntent.create(customer=customer.id)
    return JsonResponse({'client_secret': setup_intent.client_secret})

@csrf_exempt
def webhook_received(request):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.body.decode('utf-8'))

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

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
        # set up the register route, url and templates 

        # Get the customer ID from the event
        customer_id = event['data']['object']['customer']

        # Now, you have the customer_id, and you can use it to retrieve the customer from Stripe
        try:
            customer = stripe.Customer.retrieve(customer_id)
            print(f'🔔 Customer retrieved from Stripe: {customer_id}')
            
            # At this point, you can perform any additional logic with the retrieved customer data.
            # For example, store it in your database or update user information.

            # Redirect to the registration page with the ID of the Customer object.
            #return redirect('registration', customer_id=customer.id)
           
        except stripe.error.StripeError as e:
            print(f'❌ Error retrieving customer from Stripe: {e}')
            # Handle the error, possibly redirect back to the registration page with an error message


    if event["type"] == 'setup_intent.setup_failed':
        print('🔔 A SetupIntent has failed the attempt to set up a PaymentMethod.')
        # redirect back to the registration page with the error message


    return JsonResponse({'status': 'success'})

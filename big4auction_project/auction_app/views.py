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
    
    elif event["type"] == "setup_intent.succeeded":
        print('🔔 A SetupIntent has successfully set up a PaymentMethod for future use.')

    if event["type"]== 'payment_method.attached':
        print('🔔 A PaymentMethod has successfully been saved to a Customer.')

        # At this point, associate the ID of the Customer object with your
        # own internal representation of a customer, if you have one.

        # Optional: update the Customer billing information with billing details from the PaymentMethod

        #print('🔔 Customer successfully updated.')

    if event["type"] == 'setup_intent.setup_failed':
        print('🔔 A SetupIntent has failed the attempt to set up a PaymentMethod.')


    return JsonResponse({'status': 'success'})

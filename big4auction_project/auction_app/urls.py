from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_setup_intent_page, name='get_setup_intent_page'),
    path('public-key', views.get_publishable_key, name='get_publishable_key'),
    path('create-setup-intent', views.create_setup_intent, name='create_setup_intent'),
    path('webhook', views.webhook_received, name='webhook_received'),
]
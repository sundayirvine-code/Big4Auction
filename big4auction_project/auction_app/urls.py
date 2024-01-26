from django.urls import path
from . import views

urlpatterns = [
    path('register-card', views.get_setup_intent_page, name='get_setup_intent_page'),
    path('registration/<str:customer_id>', views.registration, name='registration'),
    path('public-key', views.get_publishable_key, name='get_publishable_key'),
    path('create-setup-intent', views.create_setup_intent, name='create_setup_intent'),
    path('webhook', views.webhook_received, name='webhook_received'),
    path('login', views.login_view, name='login'),
]
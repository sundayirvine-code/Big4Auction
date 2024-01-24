from django.urls import path
from .views import CreateCheckoutSessionView, ProductLandingPageView

urlpatterns = [
    path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
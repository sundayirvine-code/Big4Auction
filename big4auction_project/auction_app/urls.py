from django.urls import path
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('', ),
     path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
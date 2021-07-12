from django.urls import path

from apps.pay.views import PaymentStatusView, PayUrlView

urlpatterns = [
    path('payment/status/', PaymentStatusView.as_view()),
    path('payment/<int:order_id>/', PayUrlView.as_view()),
]

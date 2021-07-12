from django.urls import path

from apps.orders.views import OrderCommitView

urlpatterns = [
    path('orders/settlement/', OrderCommitView.as_view()),
    path('orders/commit/', OrderCommitView.as_view()),
]

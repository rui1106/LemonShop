from django.urls import path

from apps.carts.views import CartsView, ShowCartView

urlpatterns = [
    path('carts/', CartsView.as_view()),
    path('show_cart/', ShowCartView.as_view()),
    # path('show_cart/', ShowCartView.as_view()),
]

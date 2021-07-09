from django.urls import path

from apps.goods.views import CategoryView, ShopView

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('shop/', ShopView.as_view()),
]

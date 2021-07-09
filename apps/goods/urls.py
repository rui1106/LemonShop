from django.urls import path

from apps.goods.views import CategoryView, ShopView, ShopDetailView

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('shop/', ShopView.as_view()),
    path('single_product/<pk>/', ShopDetailView.as_view()),
]

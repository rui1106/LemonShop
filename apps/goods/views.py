from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin

from apps.goods.models import GoodsCategory, SKU
from apps.goods.serializer import GoodsCategoryModelSerializer, ShopModelSerializer


class CategoryView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategoryModelSerializer

    # pagination_class = PageNum


class ShopView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = ShopModelSerializer

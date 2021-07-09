from django.shortcuts import render

# Create your views here.
from django.views import View
from requests import Response
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView

from apps.goods.models import GoodsCategory, SKU
from apps.goods.serializer import GoodsCategoryModelSerializer, ShopModelSerializer


class CategoryView(ListAPIView):
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategoryModelSerializer

    # pagination_class = PageNum


class ShopView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = ShopModelSerializer


class ShopDetailView(RetrieveModelMixin, GenericAPIView):
    queryset = SKU.objects.all()
    serializer_class = ShopModelSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

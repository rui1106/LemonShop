from rest_framework import serializers

from apps.goods.models import GoodsCategory, SKU


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['name']


class ShopModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'

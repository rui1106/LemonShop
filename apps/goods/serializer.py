from rest_framework import serializers

from apps.goods.models import GoodsCategory, SKU


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class ShopModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'

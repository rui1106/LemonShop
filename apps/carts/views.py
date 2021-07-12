import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.goods.models import SKU


class CartsView(APIView):
    """购物车管理"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """添加购物车"""
        # 接收和校验参数
        json_date = json.loads(request.body)
        sku_id = json_date.get("skuid")  # 商品id
        count = json_date.get("count")  # 数量
        # 判断用户是否登录

        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "errmsg": "商品不存在"})
        try:
            count = int(count)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "errmsg": "数量错误"})

        user = request.user

        print(1111111, request.user)

        print(user.is_authenticated)

        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 新增购物车数据
            pl.hincrby('cart_%s' % user.id, sku_id, count)
            # 新增选中的状态
            pl.sadd('selected_%s' % user.id, sku_id)
            # 执行管道
            pl.execute()
            # 响应结果
            return JsonResponse({'code': 0, 'errmsg': '添加购物车成功'})
        else:
            return JsonResponse({'code': 400, 'errmsg': '请登录'})


class ShowCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            redis_conn = get_redis_connection('carts')
            redis_cart = redis_conn.hgetall('cart_%s' % user.id)
            print(user.id)
            print(redis_cart)
            # cart_selected = redis_conn.smembers('selected_%s' % user.id)
            # 将redis中的两个数据统一格式，跟cookie中的格式一致，方便统一查询
            carts = {}
            for sku_id, count in redis_cart.items():
                # print(sku_id)
                # print(count)
                carts[int(sku_id)] = {
                    'count': int(count),
                }
        else:
            return JsonResponse({'code': 400, 'errmsg': '请登录'})
        sku_ids = carts.keys()
        print(sku_ids)

        skus = SKU.objects.filter(id__in=sku_ids)

        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                # 'default_image_url': sku.default_image.url,
                'price': sku.price,
                'count': carts[sku.id]['count'],
                # 'selected': carts[sku.id]['selected'],

            })

        response = JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': sku_list})
        return response

    def delete(self, request):
        user = request.user
        body = request.body
        dict_body = json.loads(body)
        # 获取要删除商品的id
        sku_id = dict_body.get('sku_id')

        # 验证数据
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '商品不存在'})

        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hdel('cart_%s' % user.id, sku_id)
            pl.execute()

            return JsonResponse({'code': 0, 'errmsg': '删除购物车成功'})
        else:
            return JsonResponse({'code': 400, 'errmsg': '请登录'})



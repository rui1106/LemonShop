import json
from _decimal import Decimal
# from datetime import timezone
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.views import APIView

from apps.carts.models import OrderInfo, OrderGoods
from apps.goods.models import SKU
from apps.users.models import Address


class OrderCommitView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        adds = Address.objects.filter(is_deleted=False, user=user)
        # 转成字典
        addresses_list = []
        for address in adds:
            addresses_list.append({
                'id': address.id,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })

        # print(addresses_list)
        redis_conn = get_redis_connection('carts')

        carts_dict = redis_conn.hgetall('cart_%s' % user.id)
        # selected_list = redis_conn.smembers('selected_%s' % user.id)

        carts = {}
        for sku_id, count in carts_dict.items():
            # print(sku_id)
            # print(count)
            carts[int(sku_id)] = {
                'count': int(count)
            }
        # for sku_id in selected_list:
        #     count = carts_dict[sku_id]
        #     new_cart_dict[int(sku_id)] = int(count)

        try:
            skus = SKU.objects.filter(id__in=carts_dict.keys())
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '数据查询失败'})

        sku_list = []
        for sku in skus:
            print(sku)
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                # 'default_image_url': sku.default_image.url,
                'count': carts[sku.id]['count'],
                'price': sku.price
            })
        freight = Decimal('10.00')
        context = {
            'addresses': addresses_list,
            'skus': sku_list,
            'freight': freight,
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'context': context})

    def post(self, request):
        user = request.user
        json_data = json.loads(request.body)
        address_id = json_data.get('address_id')
        pay_method = json_data.get('pay_method')

        # 2 校验参数
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        try:
            address = Address.objects.get(id=address_id)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '地址查询失败'})

        if pay_method not in {OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']}:
            return JsonResponse({'code': 400, 'errmsg': '参数pay_method错误'})
        # 生成订单号 年月日时分秒+用户编号 %f 微妙  %09d表示显示为9位
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S%f') + ('%09d' % user.id)

        total_count = 0
        total_amount = 0

        freight = Decimal('10.00')

        status = OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else \
            OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address_id=address_id,
                    total_count=total_count,
                    total_amount=total_amount,
                    freight=freight,
                    pay_method=pay_method,
                    status=status,
                )
            except Exception as e:
                print(e)
                # 回滚到保存点
                # transaction.savepoint_rollback(save_id)
                return JsonResponse({'code': 400, 'errmsg': '订单保存失败'})

            # print(order)

            redis_conn = get_redis_connection('carts')
            carts_dict = redis_conn.hgetall('cart_%s' % user.id)
            carts = {}
            selected_list = []
            for sku_id, count in carts_dict.items():
                selected_list.append(sku_id)
                # print(int(count))
                carts[int(sku_id)] = int(count)

            # print(carts)
            try:
                skus = SKU.objects.filter(id__in=carts_dict.keys())
            except Exception as e:
                transaction.savepoint_rollback(save_id)
                print(e)
                return JsonResponse({'code': 400, 'errmsg': '数据查询失败'})

            try:
                for sku in skus:
                    while True:
                        # count = new_cart_dict[sku.id]
                        # if count > sku.stock:
                        #     return JsonResponse({'code': 400, 'errmsg': '库存不足'})
                        origin_stock = sku.stock
                        origin_sales = sku.sales

                        count = carts[sku.id]
                        # print(sku.ic, sku.stock)
                        if count > sku.stock:
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'code': 400, 'errmsg': '库存不足'})

                        new_stock = origin_stock - count
                        new_sales = origin_sales + count
                        result = SKU.objects.filter(id=sku.id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)

                        if result == 0:
                            continue

                        OrderGoods.objects.create(
                            order_id=order_id,
                            sku=sku,
                            count=count,
                            price=sku.price
                        )

                        order.total_count += count
                        order.total_amount += count * sku.price
                        break

                        # 回滚到保存点
                        # transaction.savepoint_rollback(save_id)
                        # return JsonResponse({'code': 400, 'errmsg': '订单商品保存失败'})
                    # order.total_count += count
                    # order.total_amount += count * sku.price

                    order.total_amount += order.freight
                    order.save()
                    print('保存成功')
            except Exception as e:
                print(e)
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'code': 400, 'errmsg': '商品订单保存失败'})
            transaction.savepoint_commit(save_id)

        redis_conn.hdel('cart_%s' % user.id, *selected_list)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'order_id': order_id})

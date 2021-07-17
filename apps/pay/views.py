from django.shortcuts import render

# Create your views here.
from alipay import AliPay, AliPayConfig
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from LemonShop import settings
from apps.carts.models import OrderInfo
from apps.pay.models import Payment


class PayUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        # 1 获取订单id
        # 2 验证订单id
        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except:
            return JsonResponse({"code": 400, 'errmsg': "没有这个订单 "})

        # 3 读取公钥和私钥
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        # 4 创建AliPay对象
        print("创建AliPay对象")
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=30)  # 可选，请求超时时间
        )
        print(order_id)

        # 5 调用支付方法
        order_string = alipay.client_api(
            "alipay.trade.page.pay",
            biz_content={
                'out_trade_no': order_id,
                # total_amount是Decimal类型  无法json序列化  这里强转为str
                'total_amount': str(order.total_amount),
                'subject': "美多商城%s" % order_id,
                'product_code': 'FAST_INSTANT_TRADE_PAY'
            },
            return_url=settings.ALIPAY_RETURN_URL  # this is optional
        )

        print("用支付方法")

        # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
        # 6 拼接一个链接
        # https://openapi.alipaydev.com/gateway.do  注意多一个dev 是沙箱测试地址
        # alipay_url = 'https://openapi.alipay.com/gateway.do?' + order_string
        alipay_url = settings.ALIPAY_URL + order_string
        print("alipay_url", alipay_url)
        # 7 返回响应

        return JsonResponse({"code": 0, 'errmsg': "ok ", "alipay_url": alipay_url})


"""
需求   接受支付成功 返回的所有参数 把订单号和交易号保存到数据库
/payment/status/?'+document.location.search
"""


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # for django users
        data = request.GET.dict()

        signature = data.pop("sign")

        # 读取公钥和私钥
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        # 创建AliPay对象
        print("创建AliPay对象")
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=30)  # 可选，请求超时时间
        )

        # verification 验证 数据
        success = alipay.verify(data, signature)
        print("success", success)
        if success:
            # 读取order_id
            order_id = data.get('out_trade_no')
            # 读取支付宝交易号
            trade_id = data.get('trade_no')
            # 保存Payment模型类数据
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )

            # 修改订单状态为待评价
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM["UNSEND"])
            print(trade_id)
            # 响应trade_id
            return JsonResponse({'code': 0, 'errmsg': 'OK', 'trade_id': trade_id})
        else:
            # 订单支付失败，重定向到我的订单
            return JsonResponse({'code': 400, 'errmsg': '非法请求'})

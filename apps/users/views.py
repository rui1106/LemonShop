import json
import re

from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.

# from requests import Response
from django.views import View
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

# http://127.0.0.1:8000/usernames/lemon/count/
from rest_framework_jwt.views import JSONWebTokenAPIView

from apps.users.models import User


class UserCountView(APIView):
    def get(self, request, name):
        count = User.objects.filter(username=name).count()
        return Response({'count': count})


# http://127.0.0.1:8000/mobiles/15340851024/count/
class MobileCountView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return Response({'count': count})


class Register(View):
    def post(self, request):
        body_byte = request.body
        body_dict = json.loads(body_byte)

        username = body_dict.get('username')
        password = body_dict.get('password')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')
        print(username, password, mobile, sms_code, allow)
        if not all([username, password, mobile, sms_code]):
            return JsonResponse({'code': '400', 'errmsg': 'register fail'})

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({"code": "400", "errmsg": "register fail"})

        redis_cli = get_redis_connection('code')
        redis_sms_code = redis_cli.get('sms_%s' % mobile)

        # 判断是否过期
        if redis_sms_code is None:
            return JsonResponse({"code": 400, 'errmsg': 'Verification code expired'})

        # 判断和用户发过来的验证码
        if redis_sms_code.decode() != sms_code:
            return JsonResponse({"code": 400, "errmsg": "sms verification code error"})

        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            return JsonResponse({"code": 400, 'errmsg': '用户保存失败,检查用户信息'})
        print("保存用户到数据库成功")
        login(request, user)

        response = JsonResponse({"code": 0, "errmsg": "ok"})
        # 把用户名保存到cookie 方便在首页显示 有效期产品决定
        response.set_cookie('username', user.username, max_age=3600 * 24 * 5)

        return response


# serializer_class = UserModelSerializer
# class LoginView(View):
#     def post(self, request):
#         body = request.body
#         dict_body = json.loads(body)
#
#         username = dict_body.get('username')
#         password = dict_body.get('password')
#         remembered = dict_body.get('remembered')
#
#         if not all([username, password]):
#             return JsonResponse({'code': 400, 'errmsg': '参数不全'})
#         if re.match('1[3-9]\d{9}', username):
#             User.USERNAME_FIELD = 'mobile'
#         else:
#             User.USERNAME_FIELD = 'username'
#         user = authenticate(username=username, password=password)
#         # print(user)
#         if user is None:
#             return JsonResponse({"code": 400, "errmsg": "用户名密码不正确"})
#         # 4. 状态保持
#         login(request, user)
#         # 5. 判断是否记住登录
#         if remembered:
#             request.session.set_expiry(3600)
#         else:
#             request.session.set_expiry(0)
#         # 6. 返回响应
#         response = JsonResponse({'code': 0, "errmsg": 'ok'})
#         # response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
#         response.set_cookie('username', user.username, max_age=3600)
#         return response


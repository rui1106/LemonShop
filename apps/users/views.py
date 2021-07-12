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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# http://127.0.0.1:8000/usernames/lemon/count/
from rest_framework_jwt.views import JSONWebTokenAPIView

from apps.users.models import User, Address


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

# '/addresses/create/'
class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        body = request.body
        data_dict = json.loads(body)

        # 2. 获取参数
        receiver = data_dict.get('receiver')
        # province_id = data_dict.get('province_id')
        # city_id = data_dict.get('city_id')
        # district_id = data_dict.get('district_id')
        place = data_dict.get('place')
        mobile = data_dict.get('mobile')
        tel = data_dict.get('tel')
        email = data_dict.get('email')

        # 3. 验证参数
        if not all([receiver, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile错误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '固定电话格式错误'})

        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({"code": 400, 'errmsg': '邮箱地址格式错误'})

        user = request.user
        try:
            address = Address.objects.create(
                user=user,
                title=receiver,
                receiver=receiver,
                # province_id=province_id,
                # city_id=city_id,
                # district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '保存数据库失败'})

        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            # "province": address.province.name,
            # "city": address.city.name,
            # "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email

        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        addresses = Address.objects.filter(user=user, is_deleted=False)
        # print(addresses)

        addresses_list = []
        for address in addresses:
            print(address)
            addresses_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                # "province": address.province.name,
                # "city": address.city.name,
                # "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
        # print(addresses_list)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': addresses_list})


# /addresses/1/
class Deladdress(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        address = Address.objects.get(id=id)
        if not address:
            return JsonResponse({'code': 400, 'errmsg': '要删除的地址不存在'})
        try:
            address.is_deleted = True
            address.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '地址删除错误'})

        return JsonResponse({'code': 0, 'errmsg': 'ok'})

    def put(self, request, id):
        body = request.body
        data_dict = json.loads(body)

        # 2. 获取参数
        receiver = data_dict.get('receiver')
        # province_id = data_dict.get('province_id')
        # city_id = data_dict.get('city_id')
        # district_id = data_dict.get('district_id')
        place = data_dict.get('place')
        mobile = data_dict.get('mobile')
        tel = data_dict.get('tel')
        email = data_dict.get('email')
        # 3. 验证参数
        if not all([receiver, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数mobile错误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '固定电话格式错误'})

        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({"code": 400, 'errmsg': '邮箱地址格式错误'})
        try:
            Address.objects.filter(id=id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                # province_id=province_id,
                # city_id=city_id,
                # district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '更新地址失败'})
        address = Address.objects.get(id=id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            # "province": address.province.name,
            # "city": address.city.name,
            # "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email

        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})

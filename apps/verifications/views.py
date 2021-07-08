from random import randint

from django.http import HttpResponse, JsonResponse

from django_redis import get_redis_connection

from django.views import View

from utils.captcha.captcha import captcha


class ImageCodeView(View):
    def get(self, request, uuid):
        print(uuid)
        text, image = captcha.generate_captcha()
        print(text)
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 120, text)

        return HttpResponse(image, content_type='image/jpeg')


class SmsCodeView(View):
    def get(self, request, mobile):
        # this.host + '/sms_codes/' + this.mobile + '/' + '?image_code=' + this.image_code+ '&image_code_id=' + this.image_code_id
        # 1. 获取参数
        image_code = request.GET.get("image_code")
        image_code_id = request.GET.get("image_code_id")

        # 2. 验证参数是否存在
        if not all([image_code, image_code_id]):
            return JsonResponse({"code": 400, "errmsg": "Parameter is not complete"})

        # 3. 验证图片验证码
        # 通过redis里面的uuid获取里面的信息
        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(image_code_id)

        # 删除图片验证码
        try:
            redis_cli.delete(image_code_id)
        except Exception as e:
            print("删除图片验证码")

        # 判断验证码是否过期
        if redis_image_code is None:
            return JsonResponse({"code": 400, "errmsg": "Verification code expired"})

        # 判断用户输入的验证码和redis里面存储的对比是否一样
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({"code": 400, "errmsg": "Image verification code error"})

        sms_code = "%06d" % randint(0, 999999)
        print("sms_code", sms_code)

        # 防止发送短信频繁
        # 1 获取"send_flag_手机号" 的值
        send_flag = redis_cli.get("send_flag_%s" % mobile)
        # send_flag_15211222

        # if 值存在 返回错误相应 过于频繁发送
        if send_flag:
            return JsonResponse({"code": 400, "errmsg": "SMS verification is sent too often"})

        # 创建Redis管道
        pl = redis_cli.pipeline()
        # 保存短信验证码到redis key的格式
        pl.setex("sms_%s" % mobile, 60, sms_code)
        pl.setex("send_flag_%s" % mobile, 60, 1)
        # 执行请求
        pl.execute()

        # SmsUtil().send_message(mobile, (sms_code, 2))
        # celery_send_sms_code.delay(mobile, sms_code)

        return JsonResponse({"code": 0, "errmsg": "ok"})

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from django.utils.translation import ugettext as _
from rest_framework_jwt.views import JSONWebTokenAPIView


class AdminJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                # 新增添加
                if not user.is_staff:
                    msg = _('User account is disabled')
                    raise serializers.ValidationError(msg)
                payload = jwt_payload_handler(user)

                return {
                    'user': user,
                    'code': 0,
                    'token': jwt_encode_handler(payload),
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class AdminJSONWebTokenView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer


admin_jwt_token = AdminJSONWebTokenView.as_view()

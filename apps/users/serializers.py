from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'mobile']

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user

# __Time__ : 2020/10/8 下午3:32
# __Author__ : '__YDongY__'

import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import UserInfo


class UserModelSerializer(ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserInfo
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if re.match(r'.+@.+', username, re.I):
            user = UserInfo.objects.filter(email=username).first()
        elif re.match(r'1[3-9][0-9]{9}', username):
            user = UserInfo.objects.filter(mobile=username).first()
        else:
            user = UserInfo.objects.filter(username=username).first()

        if user and user.check_password(password):
            # 签发token
            payload = jwt_payload_handler(user)
            self.token = jwt_encode_handler(payload)

            return attrs

        raise serializers.ValidationError({'data': '数据有误'})

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if user is None:

            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError({"detail": "존재하지 않는 사용자입니다."})
            raise serializers.ValidationError({"detail": "비밀번호가 틀렸습니다."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "사용할 수 없는 계정입니다."})

        return super().validate(attrs)

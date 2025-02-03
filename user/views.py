from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        print(token)

        return token
    
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception("존재하지 않는 사용자입니다.")


        #     return Response({"detail": "존재하지 않는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            raise Exception("비밀번호가 일치하지 않습니다.")

        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

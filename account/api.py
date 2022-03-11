from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from backend_mathcs import settings
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        response.data = {
            "error": {
                "enMessage": "Bad request!"
            }
        }

    return response


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": self.create_token(user),
            "message": "successfull",
        })

    @staticmethod
    def create_token(user):
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token


class LoginApi(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": self.create_token(user),
            "message": "successfull",
        })

    @staticmethod
    def create_token(user):
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token
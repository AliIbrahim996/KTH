from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from core.models import Documents

from core.serializer import (
    PasswordChangeSerializer,
    ChefRegistrationSerializer,
    RegistrationSerializer,
)
from rest_framework import permissions
from core.models import User


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user_serializer = RegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user_obj = user_serializer.create(request.data)
            if request.data["is_chef"] == "True":
                chef_serializer = ChefRegistrationSerializer(
                    user=user_obj, data=request.data
                )
                if chef_serializer.is_valid():
                    chef_serializer.save()
                    documents_set = request.data.pop("documents_set")
                    chef_obj = chef_serializer.instance
                    token = Token.objects.get_or_create(user=chef_obj)
                    for doc in documents_set:
                        doc_obj = Documents.objects.create(chef=chef_obj, img=doc)
                    return Response(
                        {"msg": "New chef is created!", "token": token.key}, status=status.HTTP_201_CREATED
                    )
                return Response(chef_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user_obj.save()
            user_serializer.save()
            token = Token.objects.get_or_create(user=user_obj)
            return Response(
                {"msg": "New customer is created!", "token": token.key}, status=status.HTTP_201_CREATED
            )
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if "phone_number" not in request.data or "password" not in request.data:
            return Response(
                {"msg": "Credentials missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        phone_number = request.data["phone_number"]
        password = request.data["password"]
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {"msg": "Unregistered account"}, status=status.HTTP_400_BAD_REQUEST
            )

        # if user is not None:
        if user.is_active:
            if not request.user.is_authenticated:
                if user.check_password(password):
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request, user)
                    return Response({"msg": "Login Success", "token": token.key}, status=status.HTTP_200_OK)
                return Response(
                    {"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
                )
            return Response({"msg": "Already Login Success"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": "User is unauthorized, OTP required!"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"msg": "Successfully Logged out"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            context={"request": request}, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyOTPView(APIView):
    def post(self, request):
        if request.data["is_verified"]:
            user = User.objects.get(phone_number=request.data["phone_number"])
            user.is_active = True
            user.save()
            return Response({"msg": "User is verified"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": "missing or invalid is_verified value"},
            status=status.HTTP_400_BAD_REQUEST,
        )

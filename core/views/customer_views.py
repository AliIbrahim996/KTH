from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from core.models import Documents, VerificationCode, Chef
from rest_framework import viewsets

from core.serializer import (
    PasswordChangeSerializer,
    ChefRegistrationSerializer,
    RegistrationSerializer,
    CustomerSerializer,
    ChefListSerializer,
)
from rest_framework import permissions
from core.models import User

# Required includes for TFA
from twilio.rest import Client
import random

from kitchenhome.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_MESSAGING_SERVICE_SID


def send_verification_code(phone_number):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    # Generate random code
    code = random.randint(1000, 9999)
    message = client.messages.create(
        messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID,
        body='Your verification code is {}'.format(code),
        to=phone_number
    )
    return code, message


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
                    token, _ = Token.objects.get_or_create(user=chef_obj)
                    for doc in documents_set:
                        doc_obj = Documents.objects.create(chef=chef_obj, img=doc)
                    code, message = send_verification_code(request.data["phone_number"])
                    if message.error_code is None:
                        chef_obj.user.is_active = False
                        chef_obj.user.save()
                        verification_code = VerificationCode.objects.create(code=code, user=chef_obj.user)
                        return Response(
                            {"msg": "New chef is created!", "token": token.key}, status=status.HTTP_201_CREATED
                        )
                return Response(chef_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            code, message = send_verification_code(request.data["phone_number"])
            if message.error_code is None:
                user_obj.is_active = False
                user_obj.save()
                user_serializer.save()
                verification_code = VerificationCode.objects.create(code=code, user=user_obj)
                token, _ = Token.objects.get_or_create(user=user_obj)
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

        if user.is_active:
            if not request.user.is_authenticated:
                if user.check_password(password):
                    token, _ = Token.objects.get_or_create(user=user)
                    login(request, user)
                    user_data = CustomerSerializer(user)
                    if Chef.objects.get(user=user):
                        is_chef = True
                        user_data = ChefListSerializer(Chef.objects.get(user=user))
                    else:
                        is_chef = False

                    return Response({"msg": "Login Success", "token": token.key, "user": user_data.data,
                                     "role": 2 if is_chef else 1},
                                    status=status.HTTP_200_OK)
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


class ResetPasswordView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        if request.data["phone_number"] and request.data["new_password"]:
            user = User.objects.filter(phone_number=request.data["phone_number"])
            user.set_password(request.data["new_password"])
            user.save()
            return Response({"msg": "Password rested successfully"}, status=status.HTTP_200_OK)
        return Response({"msg": "Missing phone_number or new_password fields!"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(ResetPasswordView):
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
        return Response(status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        if request.data["phone_number"] and request.data["verification_code"]:
            user = User.objects.get(phone_number=request.data["phone_number"])
            user.is_active = True
            user.save()
            return Response({"msg": "User is verified"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": "missing/invalid phone number or code"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendCodeView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request):
        if request.data["phone_number"]:
            if User.objects.get(phone_number=request.data["phone_number"]).exists():
                code, message = send_verification_code(request.data["phone_number"])
                if message.error_code is None:
                    verification_code = VerificationCode.objects.create(code=code, user=User.objects.get(
                        phone_number=request.data["phone_number"]))
                    msg = "VerificationCode is sent! code {}".format(verification_code)
                    return Response({"msg": msg}, status=status.HTTP_200_OK)
                return Response({"msg": message.error_message + ", error code: " + message.error_code},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "The user dose not exists!"}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {"msg": "missing or invalid phone number!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateProfileView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def partial_update(self, request, *args, **kwargs):
        res = super().partial_update(request, *args, **kwargs)
        res.data.update({"msg": "User is updated!"})

    def update(self, request, *args, **kwargs):
        res = super().update(request, *args, **kwargs)
        res.data.update({"msg": "User is updated!"})

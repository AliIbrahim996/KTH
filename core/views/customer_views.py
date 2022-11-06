from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.serializer import RegistrationSerializer, PasswordChangeSerializer
from rest_framework import permissions
from core.models import User


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if "phone_number" not in request.data or "password" not in request.data:
            return Response(
                {"msg": "Credentials missing"}, status=status.HTTP_400_BAD_REQUEST
            )
        #  phone_number = request.Post.get("phone_number")
        #  password = request.Post.get("password")
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response(
                {"msg": "Unregistered account"}, status=status.HTTP_400_BAD_REQUEST
            )

        # user = authenticate(request, username=phone_number, password=password)
        # if user is not None:
        if user.check_password(password):
            login(request, user)
            return Response({"msg": "Login Success"}, status=status.HTTP_200_OK)
        return Response(
            {"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
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

from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView


app_name = "core"

urlpatterns = [
    path("user/signup", RegistrationView.as_view(), name="register"),
    path("user/login", LoginView.as_view(), name="register"),
    path("user/logout", LogoutView.as_view(), name="register"),
    path("user/resetPassword", ChangePasswordView.as_view(), name="register"),
]

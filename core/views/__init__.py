from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView, \
    ResetPasswordView, VerifyCodeView, SendCodeView
from .meal_views import MealsByCategoryView, MealsByChefView, MealsViewSet, MealView
from .category_views import CategoryView
from .chef_views import ChefView, BestChefsView

__all__ = [
    "RegistrationView",
    "LoginView",
    "LogoutView",
    "ChangePasswordView",
    "MealsByCategoryView",
    "MealsByChefView",
    "MealsViewSet",
    "MealView",
    "CategoryView",
    "ChefView",
    "BestChefsView",
    "ResetPasswordView",
    "VerifyCodeView",
    "SendCodeView",
]

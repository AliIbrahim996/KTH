from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView
from .meal_views import MealsByCatecoryView, MealsByChefView, MealsViewSet, MealView
from .category_views import CategoryView

__all__ = [
    "RegistrationView",
    "LoginView",
    "LogoutView",
    "ChangePasswordView",
    "MealsByCatecoryView",
    "MealsByChefView",
    "MealsViewSet",
    "MealView",
    "CategoryView",
]

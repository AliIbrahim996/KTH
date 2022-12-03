from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView
from .meal_views import MealsByCategoryView, ChefMealsByCategoryView, MealsByChefView, MealsViewSet, MealView
from .category_views import CategoryView
from .chef_views import ChefView, BestChefsView

__all__ = [
    "RegistrationView",
    "LoginView",
    "LogoutView",
    "ChangePasswordView",
    "MealsByCategoryView",
    "ChefMealsByCategoryView",
    "MealsByChefView",
    "MealsViewSet",
    "MealView",
    "CategoryView",
    "ChefView",
    "BestChefsView",
]

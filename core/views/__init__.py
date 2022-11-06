from .chef_views import ChefList

from .meal_views import LatestMealList, ChefMealList
from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView

__all__ = [
    "RegistrationView",
    "LoginView",
    "LogoutView",
    "ChangePasswordView",
    "ChefList",
    "LatestMealList",
    "ChefMealList",
]

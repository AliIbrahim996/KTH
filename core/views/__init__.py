from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView
from .meal_views import MealsByCategoryView, ChefMealsByCategoryView, MealsByChefView, MealsViewSet, MealView
from .category_views import CategoryView, ChefCategoryView
from .chef_views import ChefView, BestChefsView
from .subscriptionViews import CustomerSubscriptionView, CustomerSubscribeChefView
from .searchViews import SearchView
from .customer_views import ResetPasswordView, SendCodeView, VerifyCodeView

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
    "ChefCategoryView",
    "ChefView",
    "BestChefsView",
    "CustomerSubscriptionView",
    "CustomerSubscribeChefView",
    "SearchView",
    "ResetPasswordView",
    "SendCodeView",
    "VerifyCodeView"
]

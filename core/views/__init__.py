from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView, ResetPasswordView, \
    SendCodeView, VerifyCodeView, UpdateProfileView
from .meal_views import MealsByCategoryView, ChefMealsByCategoryView, MealsByChefView, MealsViewSet, MealView
from .category_views import CategoryView, ChefCategoryView
from .chef_views import ChefView, BestChefsView
from .subscriptionViews import CustomerSubscribeChefView
from .searchViews import SearchView
from .cart_views import CartView
from .wishlist_view import WishListAPIView
from .location_views import LocationView, UserLocationView

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
    "CustomerSubscribeChefView",
    "SearchView",
    "ResetPasswordView",
    "SendCodeView",
    "VerifyCodeView",
    "CartView",
    "WishListAPIView",
    "LocationView",
    "UserLocationView",
    "UpdateProfileView",
]

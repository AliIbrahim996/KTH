from .customer_views import RegistrationView, LoginView, LogoutView, ChangePasswordView, ResetPasswordView, \
    SendCodeView, VerifyCodeView, UpdateProfileView
from .meal_views import TrendingMealsViewSet, MealsByCategoryView, ChefMealsByCategoryView, MealsByChefView, MealsViewSet, MealView
from .category_views import CategoryView, ChefCategoryView
from .chef_views import ChefView, BestChefsView
from .subscriptionViews import CustomerSubscribeChefView
from .searchViews import SearchView
from .cart_views import CartView
from .StripeViews import StripeViews, StripeFulfilViews
from .wishlist_view import WishListAPIView
from .location_views import LocationView, UserLocationView
from .OrderViews import OrderDetailsView
from .OrderRateView import OrderRateView

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
    "StripeViews",
    "WishListAPIView",
    "StripeFulfilViews",
    "LocationView",
    "UserLocationView",
    "UpdateProfileView",
    "OrderDetailsView",
    "TrendingMealsViewSet",
    "OrderRateView",
]

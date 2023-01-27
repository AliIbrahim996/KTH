from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view
from .views import (RegistrationView, LoginView, LogoutView, ChangePasswordView, \
                    ChefView, BestChefsView, CategoryView, MealsViewSet, MealsByCategoryView, MealsByChefView,
                    ChefMealsByCategoryView, \
                    ChefCategoryView, CustomerSubscribeChefView, SearchView, CartView, WishListAPIView, 
                    MealView, ResetPasswordView, SendCodeView, VerifyCodeView)

from .views.swagger_ui import SwaggerUITemplateView

app_name = "core"

urlpatterns = [
    path("user/signup", RegistrationView.as_view(), name="register"),
    path("user/login", LoginView.as_view(), name="register"),
    path("user/logout", LogoutView.as_view(), name="register"),
    path("user/changePassword", ChangePasswordView.as_view(), name="register"),
    path("user/resetPassword", ResetPasswordView.as_view(), name="register"),
    path("user/sendCode", SendCodeView.as_view(), name="register"),
    path("user/verifyCode", VerifyCodeView.as_view(), name="register"),
    path("chef/", ChefView.as_view(), name="chefs"),
    path("chef/<int:chef_id>/", ChefView.as_view(), name="chefs"),
    path("chef/<int:chef_id>/category/", ChefCategoryView.as_view({'get': 'list'}), name="chefs category"),
    path("chef/<int:chef_id>/category/<int:cat_id>/meals/", ChefMealsByCategoryView.as_view({'get': 'list'}),
         name="chefs Meals by category"),
    path("chef/meal/<int:pk>", MealView.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update',
                                        'patch': 'partial_update',
                                        'delete': 'destroy'})),
    path("chef/best", BestChefsView.as_view(), name="best chefs"),
    path("category", CategoryView.as_view({'get': 'list'}), name="category"),
    path("category/<int:cat_id>/meals/", MealsByCategoryView.as_view({'get': 'list'}), name="Meals by category"),
    path("category/<int:cat_id>/meals/<int:pk>/", MealsByCategoryView.as_view({'get': 'retrieve'}),
         name="Meals by category"),
    path("meal", MealsViewSet.as_view({'get': 'list'}), name="meals"),
    path("meal/<int:pk>/", MealsViewSet.as_view({'get': 'retrieve'}), name="meals"),
    path("meal/chef/<int:chef_id>/", MealsByChefView.as_view({'get': 'list'}), name="Meals by chef"),
    path("meal/chef/<int:chef_id>/<int:pk>/", MealsByChefView.as_view({'get': 'retrieve'}), name="Meals by chef"),
    path("customer/chef/subscribe", CustomerSubscribeChefView.as_view({'get': 'list'}), name="Customer subscriptions"),
    path("customer/chef/<int:chef_id>/subscribe", CustomerSubscribeChefView.as_view({'post': 'create'})),
    path("customer/chef/subscribe/<int:pk>", CustomerSubscribeChefView.as_view({'delete': 'destroy'})),
    path("search", SearchView.as_view(), name="Search"),
    path("customer/cart", CartView.as_view(), name="Cart endpoints"),
    path("wishlist/<int:meal_id>/", WishListAPIView.as_view(), name="Remove from wishlist"),
    path("wishlist/", WishListAPIView.as_view(), name="Add and list wishlist"),

    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Kitchen Home",
        description="API for end-points of Kitchen Home App",
        version="1.0.0",
        url='/core',
        urlconf='core.urls',
        permission_classes=[AllowAny],
    ), name='openapi-schema'),
    # Route TemplateView to serve Swagger UI templates.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', SwaggerUITemplateView.as_view(
        template_name='core/swagger-ui.html',
        extra_context={'schema_url': 'core:openapi-schema'}
    ), name='swagger-ui'),
]

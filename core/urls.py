from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView,\
    ChefView, BestChefsView, CategoryView, MealsViewSet, MealsByCategoryView, MealsByChefView, ChefMealsByCategoryView,\
    ChefCategoryView


app_name = "core"

urlpatterns = [
    path("user/signup", RegistrationView.as_view(), name="register"),
    path("user/login", LoginView.as_view(), name="register"),
    path("user/logout", LogoutView.as_view(), name="register"),
    path("user/resetPassword", ChangePasswordView.as_view(), name="register"),
    path("chef/", ChefView.as_view(), name="chefs"),
    path("chef/<int:chef_id>/", ChefView.as_view(), name="chefs"),
    path("chef/<int:chef_id>/category/", ChefCategoryView.as_view({'get': 'list'}), name="chefs category"),
    path("chef/<int:chef_id>/category/<int:cat_id>/meals/", ChefMealsByCategoryView.as_view({'get': 'list'}), name="chefs Meals by category"),
    path("chef/best", BestChefsView.as_view(), name="best chefs"),
    path("category", CategoryView.as_view({'get': 'list'}), name="category"),
    path("category/<int:cat_id>/meals/", MealsByCategoryView.as_view({'get': 'list'}), name="Meals by category"),
    path("category/<int:cat_id>/meals/<int:pk>/", MealsByCategoryView.as_view({'get': 'retrieve'}), name="Meals by category"),
    path("meal", MealsViewSet.as_view({'get': 'list'}), name="meals"),
    path("meal/<int:pk>/", MealsViewSet.as_view({'get': 'retrieve'}), name="meals"),
    path("meal/chef/<int:chef_id>/", MealsByChefView.as_view({'get': 'list'}), name="Meals by chef"),
    path("meal/chef/<int:chef_id>/<int:pk>/", MealsByChefView.as_view({'get': 'retrieve'}), name="Meals by chef"),

]

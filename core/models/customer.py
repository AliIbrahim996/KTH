from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError("The given phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    def create(self, phone_number, password, **extra_fields):
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    full_name = models.CharField(max_length=50, null=False, blank=False)
    user_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = PhoneNumberField(max_length=25, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=50, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
    date_created = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to="images/profile/", null=True)

    objects = UserManager()

    # is_active = False

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.full_name

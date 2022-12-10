from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager as DjangoUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(DjangoUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError("The given phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
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

        return self._create_user(phone_number, password, **extra_fields).save()

    def create(self, phone_number, password, **extra_fields):
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):

    full_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = PhoneNumberField(max_length=25, null=False, blank=False, unique=True)
    profile_img = models.ImageField(upload_to="images/profile/", null=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.full_name

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.role = User.ADMIN
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    STAKEHOLDER = 2
    MANAGER = 3
    ANALYST = 4
    CONSULTANT = 5
    CLIENT = 6

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (STAKEHOLDER, "Stakeholder"),
        (MANAGER, "Manager"),
        (ANALYST, "Analyst"),
        (CONSULTANT, "Consultant"),
        (CLIENT, "Client"),
    )

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="first name", max_length=255, blank=True)
    last_name = models.CharField(verbose_name="last name", max_length=255, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CLIENT)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

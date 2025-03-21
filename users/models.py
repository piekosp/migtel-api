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
        user.is_active = True
        user.role = User.ADMIN
        user.save()
        return user


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role__in=[User.ANALYST, User.CONSULTANT])


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = "ADMIN"
    STAKEHOLDER = "STAKEHOLDER"
    MANAGER = "MANAGER"
    ANALYST = "ANALYST"
    CONSULTANT = "CONSULTANT"
    CLIENT = "CLIENT"

    MANAGER_ROLES = [ADMIN, MANAGER]
    EMPLOYEE_ROLES = [ANALYST, CONSULTANT]

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
    role = models.CharField(max_length=11, choices=ROLE_CHOICES, default=CLIENT)
    project = models.ForeignKey(
        "companies.Project", null=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    employees = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

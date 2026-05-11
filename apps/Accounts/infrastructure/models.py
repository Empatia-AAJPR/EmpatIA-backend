from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.Accounts.domain.rules import UserRules
from apps.Accounts.infrastructure.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False)

    name = models.CharField(max_length=225)
    email = models.CharField(max_length=220, unique=True)
    password = models.CharField(max_length=12)
    rule = models.CharField(
        max_length=20, choices=UserRules, default=UserRules.PENDING
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'


class Token(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    hash_token = models.CharField(max_length=190)
    user = models.ForeignKey(
        'Accounts.User', on_delete=models.CASCADE, null=True, blank=True
    )
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField()
    revoked = models.BooleanField()

    class Meta:
        db_table = 'refresh_token'

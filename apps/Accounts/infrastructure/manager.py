from uuid import uuid4

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def __create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email required')

        if not extra_fields.get('id'):
            extra_fields['id'] = uuid4()

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fiels):
        extra_fiels.setdefault('is_staff', False)
        extra_fiels.setdefault('is_superuser', False)
        return self.__create_user(email, password, **extra_fiels)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.__create_user(email, password, **extra_fields)

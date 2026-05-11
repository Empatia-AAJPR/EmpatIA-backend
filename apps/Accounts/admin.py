from django.contrib import admin

from apps.Accounts.infrastructure.models import User


admin.site.register(User)

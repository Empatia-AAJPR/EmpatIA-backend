from django.db import models


class UserRules(models.TextChoices):
    PENDING = 'PENDING', 'pending'
    STUDENT = 'STUDENT', 'student'
    COORDINATOR = 'COORDINATOR', 'coordinator'

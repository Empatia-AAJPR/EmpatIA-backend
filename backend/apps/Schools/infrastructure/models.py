from uuid import uuid4

from django.db import models


class School(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=80)
    cnpj = models.CharField(max_length=20, null=False)
    logo = models.ImageField(upload_to='logos', null=True)
    gre = models.CharField(max_length=60)

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'schools'


class NucleosGroup(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100)
    school = models.ForeignKey(
        'Schools.School',
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'nucleos_group'

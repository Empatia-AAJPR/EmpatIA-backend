from uuid import uuid4

from django.db import models


class Student(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField('Accounts.User', on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        'Classroom.Classroom', on_delete=models.SET_NULL, null=True, blank=True
    )
    date_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to='photos/')
    vector_facial = models.JSONField(null=True)

    class Meta:
        db_table = 'students'


class Coordinator(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField('Accounts.User', on_delete=models.CASCADE)
    nucleos_group = models.ForeignKey(
        'Schools.NucleosGroup', on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'coordinator'


class Director(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField('Accounts.User', on_delete=models.CASCADE)

    school = models.OneToOneField(
        'Schools.School', on_delete=models.CASCADE, null=True
    )

    class Meta:
        db_table = 'director'

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from psycopg2 import Binary

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=255, unique=True)

    is_admin =models.BinaryField(default=bytes(False))
    is_active = models.BinaryField(default=bytes(True))
    is_superuser = models.BinaryField(default=bytes(False))
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin
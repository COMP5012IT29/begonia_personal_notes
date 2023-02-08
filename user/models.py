from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=30, unique=True)

    @property
    # This field needs to be added to the customized class if simplejwt is used
    def is_authenticated(self):
        return True


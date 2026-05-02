from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Ide jöhetnek később az extra mezők, pl. maradt szabadnapok száma
    pass

    def __str__(self):
        return self.username

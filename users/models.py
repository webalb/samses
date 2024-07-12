from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# creating a custome user model to allow us to keep track of different
#  types of users login/register into our system
class CustomUser(AbstractUser):
    pass
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self) -> str:
        return f'Profile of {{ self.user.username }}'
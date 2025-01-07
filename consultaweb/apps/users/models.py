from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class CustomUser(AbstractUser):
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access' : str(refresh.access_token),
        }
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  #changed name to avoid conflicts
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  #changed name to avoid conflicts
        blank=True,
    )
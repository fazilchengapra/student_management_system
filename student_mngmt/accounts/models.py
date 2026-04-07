from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    date_of_join = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.username
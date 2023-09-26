from django.db import models
from django.contrib.auth.models import User



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    treats = models.ManyToManyField("self", 
                                    related_name="treated_by",
                                    blank = True,
                                    symmetrical=False)
    def __str__(self):
        return self.user.username


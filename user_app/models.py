from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# customusers/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Additional fields
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    # Add related names to avoid clashes
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    # ... other fields as needed

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    phoneNo = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def get_sex_display(self):
        return dict(self.GENDER_CHOICES).get(self.sex, '')

    required = {'sex', 'email', 'firstName'}
    def __str__(self):
        return self.firstName


class PatientDetails(models.Model):
    patientID = models.OneToOneField(Patient, on_delete=models.CASCADE)
    dob = models.DateField()
    cp = models.IntegerField()
    trestbps = models.IntegerField()
    chol = models.IntegerField()
    fps = models.BooleanField()
    restech = models.IntegerField()
    thalach = models.IntegerField()
    exang = models.BooleanField()
    oldpeak = models.DecimalField(max_digits=5, decimal_places=2)
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()
    target = models.BooleanField()
    dateModified = models.DateTimeField()






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    phone_number = models.CharField(max_length=13, blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    treats = models.ManyToManyField(Patient, 
                                    related_name="treated_by",
                                    blank=True,
                                    symmetrical=False)
    
    date_modified = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Patient.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        profile = instance.profile
        profile.save()
        
        # Check if there are any treats (patients) associated with the profile
        if profile.treats.exists():
            # Save each associated patient
            for patient in profile.treats.all():
                patient.save()
    except Profile.DoesNotExist:
        # Create a Profile object if it doesn't exist
        profile = Profile.objects.create(user=instance)
        
        # Create a Patient object if it doesn't exist
        Patient.objects.create(user=instance)

# Note: Make sure to remove the duplicate @receiver(post_save, sender=User) decorator.

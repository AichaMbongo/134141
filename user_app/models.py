from django.db import models
from datetime import date
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
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=60)
    phoneNo = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def get_sex_display(self):
        return dict(self.GENDER_CHOICES).get(self.sex, '')

    required = {'sex', 'email', 'firstName'}

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class PatientDetails(models.Model):
    GENDER_CHOICES = (
        ('0', 'Male'),
        ('1', 'Female'),
    )

    CHOICES = (
        ('0', '  less than 120 mg/dl'),
        ('1', '  greater than 120 mg/dl'),
    )

    EXANG = (
        ('0', 'Absence'),
        ('1', 'Presence'),
    )
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
  

    # sex = models.BooleanField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True)

    def get_sex_display(self):
        return dict(self.GENDER_CHOICES).get(self.sex, '')
    cp = models.IntegerField(null=True, blank=True)
    trestbps = models.IntegerField(null=True, blank=True)
    chol = models.IntegerField(null=True, blank=True)
    def get_fbs_display(self):
        return dict(self.CHOICES).get(self.fbs, '')
    fbs  = models.CharField(max_length=1, choices=CHOICES,null=True, blank=True)
    restecg = models.IntegerField(null=True, blank=True)
    thalach = models.IntegerField(null=True, blank=True)
    #  exang= models.BooleanField(null=True, blank=True)
    exang = models.CharField(max_length=1, choices=EXANG,null=True, blank=True)
    oldpeak = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    slope = models.IntegerField(null=True, blank=True)
    ca = models.IntegerField(null=True, blank=True)
    thal = models.IntegerField(null=True, blank=True)
    target = models.BooleanField(null=True, blank=True)
    dateModified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient.firstName} {self.patient.lastName} Details"

class PatientVitals(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
  # Vitals measured by the nurse
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    dateModified = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.patient.firstName} {self.patient.lastName} Details"






    
class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medications = models.TextField()
    lifestyle_changes = models.TextField()
    follow_up_date = models.DateField()
    additional_notes = models.TextField()
    pdf_file = models.FileField(upload_to='pdf_files/', blank=True, null=True)

    def __str__(self):
        return f"Treatment Plan for {self.patient.firstName} {self.patient.lastName}"

    class Meta:
        ordering = ['-id']

@receiver(post_save, sender=Patient)
def create_or_update_patient_details(sender, instance, created, **kwargs):
    """
    Signal receiver function to create or update PatientDetails when a Patient is saved.

    Args:
        sender: The sender model class (Patient in this case).
        instance: The instance of the sender model being saved.
        created: A boolean indicating whether the instance was just created.
    """
    # Get or create the associated PatientDetails instance
    patient_details, created = PatientDetails.objects.get_or_create(patient=instance)

    # Provide a default value for dob if it's not set


    # Save the PatientDetails instance
    patient_details.save()




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('secretary', 'Secretary'),
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
        ('labTech', 'Lab Technician'),
        ('unassigned', 'Unassigned'),
    ]
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default= "unassigned")
    is_approved = models.BooleanField(default=False)

    
    phone_number = models.CharField(max_length=13, blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)

    
    on_leave = models.BooleanField(default=False) 
    date_modified = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        profile = instance.profile
        profile.save()
        
        # # Check if there are any treats (patients) associated with the profile
        # if profile.treats.exists():
        #     # Save each associated patient
        #     for patient in profile.treats.all():
        #         patient.save()
    except Profile.DoesNotExist:
        # Create a Profile object if it doesn't exist
        profile = Profile.objects.create(user=instance)
        
        # Create a Patient object if it doesn't exist
        Patient.objects.create(user=instance)
        



class DoctorPatientRel(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    time = models.TimeField()
    purpose = models.TextField()

    def __str__(self):
        return f"{self.patient} - Dr. {self.doctor.user.username} - {self.date} {self.time}"
    

    
# class HealthRecord(models.Model):
#     patient = models.ForeignKey(User, on_delete=models.CASCADE)
#     test_name = models.CharField(max_length=255)
#     result_explanation = models.TextField()

#     def __str__(self):
#         return f"{self.patient.username} - {self.test_name}"
    
class PredictionResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.CharField(max_length=255)
    result = models.TextField()
    purpose = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient.firstName}'s {self.test} Result"
    

class DoctorReport(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    # Add other fields for the doctor's report


class LabTest(models.Model):
    PATIENT_STATUS_CHOICES = [
        ('awaiting', 'Awaiting Test'),
        ('completed', 'Test Completed'),
        ('noNeed', 'No need for test'),
    ]

    TEST_TYPE_CHOICES = [
        ('typeA', 'CVD prediction'),
        ('typeB', 'Vitals'),
        ('typeC', 'X-ray'),
        # Add more test types as needed
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES, default='typeA')
    test_date = models.DateField(auto_now_add=True)
    patient_name = models.CharField(max_length=100)
    # other fields...

    status = models.CharField(
        max_length=20,
        choices=PATIENT_STATUS_CHOICES,
        default='noNeed',
    )

@receiver(post_save, sender=Patient)
def create_lab_test(sender, instance, created, **kwargs):
    if created:
        LabTest.objects.create(
            patient=instance,
            test_type='typeA',  # Adjust this as needed
            patient_name=f'{instance.firstName} {instance.lastName}',
            status='noNeed'
        )

class DoctorComments(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)

    patient_vitals = models.ForeignKey(PatientVitals, on_delete=models.CASCADE, related_name='comments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a one-to-one relationship with the doctor
    comments = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments for {self.patient_vitals.patient} by {self.doctor.username}"
from django.db import models
from django.contrib.auth.models import User



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    userID = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # This field represents staff status
    is_superuser = models.BooleanField(default=False)  # Add this field
   
    objects = CustomUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    phoneNo = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    last_login = models.DateTimeField(null=True, blank=True)

    def get_sex_display(self):
        return dict(self.GENDER_CHOICES).get(self.sex, '')

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    # Define unique related names to avoid conflicts
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )


class Patient(models.Model):
    patientID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    phoneNo = models.CharField(max_length=20)
    sex = models.BooleanField()

class Prediction(models.Model):
    predictionID = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    predictionDate = models.DateTimeField()
    result = models.IntegerField()

class UserRole(models.Model):
    userRoleID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('User', on_delete=models.CASCADE)
    roleID = models.ForeignKey('Role', on_delete=models.CASCADE)

# class User(models.Model):
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )

#     userID = models.AutoField(primary_key=True)
#     firstName = models.CharField(max_length=20)
#     lastName = models.CharField(max_length=20)
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100)
#     phoneNo = models.CharField(max_length=20)
#     sex = models.CharField(max_length=1, choices=GENDER_CHOICES)

#     def get_sex_display(self):
#         return dict(self.GENDER_CHOICES).get(self.sex, '')

#     def __str__(self):
#         return f"{self.firstName} {self.lastName}"

class Profile(models.Model):
    doctor= models.OneToOneField(User, on_delete=models.CASCADE)
    treats = models.ManyToManyField("self", related_name="treated_by",
                                    blank = True,
                                    symmetrical=False)
    def __str__(self):
        return self.doctor.firstName

class DoctorPatientRel(models.Model):
    relationID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

class TreatmentPlan(models.Model):
    planID = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctorID = models.ForeignKey(User, on_delete=models.CASCADE)
    planDate = models.DateTimeField()
    content = models.TextField()

class Role(models.Model):
    roleID = models.AutoField(primary_key=True)
    roleName = models.CharField(max_length=20)
    Desc = models.CharField(max_length=100)

class PatientDetails(models.Model):
    detailsID = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
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
    date = models.DateTimeField()

class Report(models.Model):
    reportID = models.AutoField(primary_key=True)
    reportTitle = models.CharField(max_length=100)
    reportContent = models.TextField()
    userID = models.IntegerField()
    predictionID = models.IntegerField()
    detailsID = models.IntegerField()
    generatedDate = models.DateTimeField()


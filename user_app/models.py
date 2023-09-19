from django.db import models

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

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phoneNo = models.CharField(max_length=20)
    sex = models.BooleanField()

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


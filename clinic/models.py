from django.db import models

# Create your models here.
class doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    hospital = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    consultation_fee = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.doctor_name


class Appointments(models.Model):
    patient_name = models.CharField(max_length=100)
    
    phone = models.CharField(max_length=15)
    doctor_id = models.IntegerField()
    appointment_date = models.DateField()
    token_number=models.PositiveIntegerField(editable=False)
    appointment_time = models.TimeField(editable=False, null=True)  
    problem = models.TextField()
    status = models.CharField(max_length=20,default="pending")
    prescription = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient_name
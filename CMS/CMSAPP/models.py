from django.db import models
from managers import UserManager
from datetime import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

#admin
#departments
class Department(models.Model):
    department_name = models.CharField(max_length=250,null=False,blank=False)
class Qualification(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=False)
    name = models.CharField(max_length=250,null=False,blank=False)
    is_active = models.BooleanField(default=True)
#employee info
class User(AbstractBaseUser,PermissionsMixin):
    Admin = 1
    Receptionist = 2
    Doctor = 3
    Pharmacist = 4
    LabTechnician = 5
    Inventory = 6
    
    ROLE_CHOICES = (
        (Admin,'Admin'),
        (Receptionist,'Receptionist'),
        (Doctor,'Doctor'),
        (Pharmacist,'Pharmacist'),
        (LabTechnician,'LabTechnician'),
        (Inventory,'Inventory')
    )
    emp_id = models.AutoField(primary_key=True,blank=False,null=False)
    first_name = models.CharField(max_length=30,null=False,blank=False)
    last_name = models.CharField(max_length=30,blank=False,null=True)
    address = models.CharField(max_length= 250,null=False,blank=False)
    dob = models.DateField(null=False,blank=False)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="departments")
    qualification = models.ForeignKey(Qualification,on_delete=models.CASCADE,related_name="qualifications")
    date_of_joining = models.DateField(null=False,blank=False)
    email = models.EmailField(max_length=50,null=False,blank=False,unique=True)
    password = models.CharField(max_length=128,blank=False)
    role = models.PositiveBigIntegerField(choices=ROLE_CHOICES,blank=False,null=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    created_date = models.DateField(null=False,default=datetime.date.today())

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['firstname','lastname','dob','qualification','password','role','is_superadmin']

    def employeeId():
        pass


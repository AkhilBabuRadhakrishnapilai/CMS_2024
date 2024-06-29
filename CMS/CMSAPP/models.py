from django.db import models
from .managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin,Group,Permission
# Create your models here.

#admin
#departments
class Department(models.Model):
    department_name = models.CharField(max_length=250,null=False,blank=False)

    def _str_(self):
        return self.department_name
    
class Qualification(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=False)
    qualification = models.CharField(max_length=250,null=False,blank=False)
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.qualification
    
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
    emp_id = models.CharField(primary_key=True,editable=False,unique=True,max_length=10)
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
    created_date = models.DateField(null=False,auto_now_add=True)
    groups = models.ManyToManyField(Group,related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name','dob','password','role']

    def save(self,*args,**kwargs):
        if not self.emp_id:
            last_emp_id = User.objects.all().order_by('emp_id').last()
            if last_emp_id:
                last_id = int(last_emp_id.emp_id.split('Emp')[-1])
                new_id = last_id + 1
            else:
                new_id = 1000
            self.emp_id = f'Emp{new_id}'
        super(User,self).save(*args,**kwargs)

    def _str_(self):
        return f'User {self.emp_id} - {self.first_name}'

#specialization
class Specialization(models.Model):
    dept = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="departmentz")
    specialization = models.CharField(max_length=100,blank=False,null=False)

    def _str_(self):
        return self.specialization
#doctors
class Doctors(models.Model):
    doc_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE,related_name="specializations")

    def _str_(self):
        return self.user_id.first_name
    



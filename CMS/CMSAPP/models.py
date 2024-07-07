from django.db import models
from .managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin,Group,Permission
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
# Create your models here.

#admin
#departments
class Department(models.Model):
    department_name = models.CharField(max_length=250,blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.department_name

class Qualification(models.Model):
    qualification = models.CharField(max_length=250,null=False,blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.qualification

class Roles(models.Model):
    role_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.role_name

#specialization
class Specialization(models.Model):
    specialization = models.CharField(max_length=100,blank=False)

    def __str__(self):
        return self.specialization

class Gender(models.Model):
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.gender
    
#employee info
class User(AbstractBaseUser,PermissionsMixin):
    emp_id = models.CharField(primary_key=True,editable=False,unique=True,max_length=10)
    first_name = models.CharField(max_length=30,null=False,blank=False)
    last_name = models.CharField(max_length=30,blank=False,null=True)
    address = models.CharField(max_length= 250,blank=False)
    dob = models.DateField(null=False,blank=False)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE,related_name="genders")
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="departments")
    qualification = models.ForeignKey(Qualification,on_delete=models.CASCADE,related_name="qualifications")
    specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE,related_name="specialisations")
    date_of_joining = models.DateField(null=False,blank=False)
    email = models.EmailField(max_length=50,null=False,blank=False,unique=True)
    password = models.CharField(max_length=128,blank=False)
    role = models.ForeignKey(Roles,null=False,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_date = models.DateField(null=False,auto_now_add=True)
    groups = models.ManyToManyField(Group,related_name='custom_user_groups',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions',blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name','dob','password','is_staff']

    def save(self,*args,**kwargs):

        if not self.emp_id:
            last_emp_id = User.objects.all().order_by('emp_id').last()
            if last_emp_id:
                last_id = int(last_emp_id.emp_id.split('Emp')[-1])
                new_id = last_id + 1
            else:
                new_id = 1000
            self.emp_id = f'Emp{new_id}'
        super().save(*args,**kwargs)

    def __str__(self):
        return f'User {self.emp_id} - {self.first_name}'


#doctors
class Doctors(models.Model):
    doc_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    dept = models.ForeignKey(Department,on_delete=models.CASCADE,related_name="depts")
    specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE,related_name="specializations")

    def __str__(self):
        return self.user_id.first_name
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        
#stock_management models
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_active =models.BooleanField(default=True,null=False)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    )
    item_name = models.CharField(max_length=100,null=True)
    category = models.CharField(max_length=100,null=True)
    ordered_quantity = models.PositiveIntegerField(null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField()
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='PENDING')
    is_active =models.BooleanField(default=True,null=False)
    def __str__(self):
        return f"Order {self.id} - {self.supplier.name}"
    


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField()
    purchase_date = models.DateField()
    warranty_expiry = models.DateField()
    is_active =models.BooleanField(default=True,null=False)

    def __str__(self):
        return self.name

    def is_below_reorder_level(self):
        return self.quantity <= self.reorder_level
    
class MiscellaneousItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField()
    is_active =models.BooleanField(default=True,null=False)

    def __str__(self):
        return self.name

    def is_below_reorder_level(self):
        return self.quantity <= self.reorder_level
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    type_medicine = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    storage_requirements = models.CharField(max_length=255)
    stock = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    reorder_level = models.IntegerField(null=True, blank=True, default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    is_active =models.BooleanField(default=True,null=False)
    def __str__(self):
        return self.name
    
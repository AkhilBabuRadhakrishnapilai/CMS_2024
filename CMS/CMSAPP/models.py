from django.db import models
from django.utils import timezone
from .managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin,Group,Permission
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client
import phonenumbers
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import check_password as django_check_password

# Create your models here.

#admin
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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.specialization

class Gender(models.Model):
    gender = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.gender
    
#employee info
class User(AbstractBaseUser,PermissionsMixin):
    emp_id = models.CharField(primary_key=True,editable=False,unique=True,max_length=10)
    first_name = models.CharField(max_length=30,null=False,blank=False)
    last_name = models.CharField(max_length=30,blank=False,null=True)
    address = models.CharField(max_length= 250,blank=False)
    dob = models.DateField(null=False,blank=False)
    contact_number = models.CharField(max_length=10,null=False,blank=True,default=0)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE,related_name="genders")
    qualification = models.ForeignKey(Qualification,on_delete=models.CASCADE,related_name="qualifications")
    date_of_joining = models.DateField(null=True,blank=False)
    email = models.EmailField(max_length=50,null=False,blank=False,unique=True)
    password = models.CharField(max_length=128,blank=False,default="clinics")
    role = models.ForeignKey(Roles,null=False,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_date = models.DateField(null=False,auto_now_add=True)
    groups = models.ManyToManyField(Group,related_name='custom_user_groups',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='custom_user_permissions',blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['first_name','last_name','dob','password','is_staff']


    def check_password(self, raw_password):
        return super().check_password(raw_password)   

    

    def save(self,*args,**kwargs):
        # Only hash the password if it's being created or changed
        if self.pk is None:
            self.set_password(self.password)  # Hash password for new users

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


# doctors
class Doctors(models.Model):
    doc_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE,related_name="specializations")
    fees = models.PositiveSmallIntegerField(null=False,blank=False,default=0)

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
    
# receptionist models

class Counter(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.PositiveIntegerField(default=0)

def get_next_counter(name):
    counter, created = Counter.objects.get_or_create(name=name)
    counter.count += 1
    counter.save()
    return counter.count

def generate_opid():
    count = get_next_counter('patient_opid')
    return f"OP_{count:02d}"

def generate_token():
    count = get_next_counter('appointment_token')
    return f"Token {count}"

class patient_details(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    opid = models.CharField(max_length=10, default=generate_opid, unique=True, editable=False)
    name = models.CharField(max_length=50, null=True)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE,related_name="genders")
    dob = models.DateField(null=True, blank=True)  # Date of birth
    age = models.PositiveIntegerField(null=True, blank=True)  # Age
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.opid})"

    def save(self, *args, **kwargs):
        # Calculate age if dob is provided
        if self.dob:
            self.age = timezone.now().year - self.dob.year
        super(patient_details, self).save(*args, **kwargs)


class BookAppointment(models.Model):
    TIME_SLOT_CHOICES = [
        ('09:00-09:30', '09:00-09:30 AM'),
        ('09:30-10:00', '09:30-10:00 AM'),
        ('10:00-10:30', '10:00-10:30 AM'),
        ('11:00-11:30', '11:30-12:00 PM')
        # Add more time slots as needed
    ]
    
    patient = models.ForeignKey(patient_details, related_name='appointments', on_delete=models.CASCADE, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name="booked_appointments")
    doctor =  models.ForeignKey(Doctors,related_name='doctor',on_delete=models.CASCADE,null=True)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=11, choices=TIME_SLOT_CHOICES, null=True)
    token = models.CharField(max_length=20, default=generate_token, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=True)

    def __str__(self):
        patient_name = self.patient.name if self.patient else 'Unknown Patient'
        doctor_name = self.doctor.user_id.first_name if self.doctor and self.doctor.user_id else 'Unknown Doctor'
        return f"Appointment for {patient_name} with Dr. {doctor_name} on {self.appointment_date} at {self.time_slot}"
    
    def save(self, *args, **kwargs):
        # Check if there are already 5 appointments for the given time slot
        existing_appointments = BookAppointment.objects.filter(
            appointment_date=self.appointment_date,
            time_slot=self.time_slot
        ).count()
        
        if (existing_appointments >= 5) and self.is_active:
            raise ValidationError(f"The time slot {self.time_slot} on {self.appointment_date} is fully booked.")
        
        super().save(*args, **kwargs)


@receiver(post_save, sender=BookAppointment)
def send_token_on_appointment_save(sender, instance, created, **kwargs):
    if created:
        send_token_to_patient(instance)


def send_token_to_patient(appointment):
    account_sid = 'AC9561c6cec28f103fe4cbbf0e58edd3b2'
    auth_token = '6a986f3297bb2e554c4e5c1d66143da7'
    client = Client(account_sid, auth_token)

    message = None  # Initialize the variable to avoid UnboundLocalError
    try:
        if appointment.patient is not None and appointment.patient.mobile is not None:
            mobile_number = phonenumbers.parse(appointment.patient.mobile, "IN")
            formatted_number = phonenumbers.format_number(mobile_number, phonenumbers.PhoneNumberFormat.E164)
            message = client.messages.create(
                body=f"Dear {appointment.patient.name}, your appointment token is {appointment.token}. Appointment with Dr. {appointment.doctor} on {appointment.appointment_date} at {appointment.time_slot}.",
                from_='+13603104099',  # Your Twilio number
                to=formatted_number
            )
        else:
            if appointment.patient is None:
                print("Appointment patient is missing.")
            elif appointment.patient.mobile is None:
                print("Patient's mobile number is missing.")
    except phonenumbers.NumberParseException:
        raise ValidationError(f"Invalid phone number: {appointment.patient.mobile}")

    if message:
        return message.account_sid
    else:
        return None  # Handle this case appropriately
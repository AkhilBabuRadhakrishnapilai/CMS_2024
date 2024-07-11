from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Qualification)
admin.site.register(User)
admin.site.register(Specialization)
admin.site.register(Doctors)
admin.site.register(Roles)
admin.site.register(Gender)
admin.site.register(Supplier)
admin.site.register(Order)

admin.site.register(Equipment)
admin.site.register(MiscellaneousItem)
admin.site.register(Medicine)

admin.site.register(patient_details)
admin.site.register(BookAppointment)
admin.site.register(Counter)

#doctor admin

admin.site.register(Diagnosis)
admin.site.register(TestPrescribed)
admin.site.register(MedPrescribed)
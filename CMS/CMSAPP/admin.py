from django.contrib import admin
from .models import *
from .models import patient_details
# Register your models here.
admin.site.register(patient_details)
admin.site.register(BookAppointment)
admin.site.register(NewTest)
admin.site.register(TestPrescribed)
admin.site.register(Diagnosis)
admin.site.register(LiveTest)
admin.site.register(Qualification)
admin.site.register(Specialization)
admin.site.register(User)
admin.site.register(Doctors)


admin.site.register(Supplier)
admin.site.register(Order)

admin.site.register(Equipment)
admin.site.register(MiscellaneousItem)
admin.site.register(Medicine)
admin.site.register(Counter)
admin.site.register(Report)

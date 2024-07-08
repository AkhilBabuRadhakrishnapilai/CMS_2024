from django.contrib import admin

from .models import  Diagnosis,patient_details,Department,Specialization,Qualification,BookAppointment,NewTest,TestPrescribed,LiveTest,User,Doctors
# Register your models here.
admin.site.register(patient_details)
admin.site.register(BookAppointment)
admin.site.register(NewTest)
admin.site.register(TestPrescribed)
admin.site.register(Diagnosis)
admin.site.register(LiveTest)
admin.site.register(Department)
admin.site.register(Qualification)
admin.site.register(Specialization)
admin.site.register(User)
admin.site.register(Doctors)


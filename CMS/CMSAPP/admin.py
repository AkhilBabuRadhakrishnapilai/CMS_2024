from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Qualification)
admin.site.register(User)
admin.site.register(Specialization)
admin.site.register(Doctors)
admin.site.register(Roles)
admin.site.register(Gender)

#doctor admin

admin.site.register(Diagnosis)
admin.site.register(TestPrescribed)
admin.site.register(MedPrescribed)
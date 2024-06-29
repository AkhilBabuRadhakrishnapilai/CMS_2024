from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Qualification)
admin.site.register(User)
admin.site.register(Specialization)
admin.site.register(Doctors)
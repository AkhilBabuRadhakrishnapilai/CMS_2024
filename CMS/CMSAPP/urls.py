from django.urls import path
from .views import *

urlpatterns = [
    path('addemployee/',EmployeeCRUD.as_view()),
    path('employeelist/',EmployeeCRUD.as_view()),
    path('edit/<str:emp_id>',EmployeeCRUD.as_view()),
    path('disable/<str:emp_id>',EmployeeCRUD.as_view()),
    path('login',Login.as_view())
]
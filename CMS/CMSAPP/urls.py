from django.urls import path
from .views import *

urlpatterns = [
    path('addemployee/',EmployeeCRUD.as_view()),
    path('employeelist/',EmployeeCRUD.as_view()),
    path('edit/<str:emp_id>',EmployeeCRUD.as_view()),
    path('disable/<str:emp_id>',EmployeeCRUD.as_view()),
    path('login',Login.as_view()),
    # departments
    # path('departments/',GetAllDepartments.as_view()),
    #qualification
    path('qualifications/',GetAllQualifications.as_view()),
    #specialization
    path('specialization/',GetAllSpecializations.as_view()),
    #gender
    path('gender/',GetAllGenders.as_view()),
    #role
    path('roles/',GetAllRoles.as_view()),
    #change password
    path('changepassword/',ChangePassword.as_view()),


    #doctor url
    # path('appointment_list', AppointmentListView.as_view()),
    path('diagnosis_list',diagnosis_list),
    path('diagnosis_info/<int:passed_id>',diagnosis_info),
    path('testPrescribed_list',testPrescribed_list),
    path('testPrescribed_info/<int:passed_id>',testPrescribed_info),
    path('medPrescribed_list',medPrescribed_list),
    path('medPrescribed_info/<int:passed_id>',medPrescribed_info),
    path('list_of_test',list_of_test),
    path('list_of_medicine',list_of_medicine)

]
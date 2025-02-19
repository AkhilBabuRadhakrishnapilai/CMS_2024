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
    # receptionist urls
    path('patient_list',PatientListView.as_view()),
    path('patient_list/<str:opid>',GetOp.as_view()),
    path('patient_info/<int:passed_id>',PatientInfoView.as_view()),
    # path('search_patient/<int:search_Patient>',search_patient),
    path('search_info/<str:search_patient>',SearchPatientView.as_view()),
    path('appointment_list',AppointmentListView.as_view()),
    path('appointment_info/<int:passed_id>',AppointmentInfoView.as_view()),
    path('search_appointment/<str:search_appoint>',SearchAppointmentView.as_view()),
    path('specialization',SpecializationList.as_view()),
    path('doctors',DoctorList.as_view()),
    path('token',GetToken.as_view()),
    path('changepassword/',ChangePassword.as_view()),
    path('suppliers', supplier_list, name='supplier-list'),
    path('suppliers/<int:passed_id>', supplier_edit, name='supplier-edit'),
    path('orders', order_list, name='order_list'),
    path('orders/<int:passed_id>', order_edit, name='orders-edit'),
    path('equipments', equipment_list, name='equipment_list'),
    path('equipments/<int:passed_id>', equipment_edit, name='equipment_edit'),
    path('MiscellaneousItem', MiscellaneousItem_list, name='MiscellaneousItem_list'),
    path('MiscellaneousItem/<int:passed_id>', MiscellaneousItem_edit, name='MiscellaneousItem_edit'),
    path('Medicine', Medicine_list, name='Medicine_list'),
    path('Medicine/<int:passed_id>', Medicine_edit, name='Medicine_edit')
]
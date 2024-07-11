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
    path('suppliers', supplier_list, name='supplier-list'),
    path('suppliers/<int:passed_id>', supplier_edit, name='supplier-edit'),
    path('orders', order_list, name='order_list'),
    path('orders/<int:passed_id>', order_edit, name='orders-edit'),
    path('equipments', equipment_list, name='equipment_list'),
    path('equipments/<int:passed_id>', equipment_edit, name='equipment_edit'),
    path('MiscellaneousItem', MiscellaneousItem_list, name='MiscellaneousItem_list'),
    path('MiscellaneousItem/<int:passed_id>', MiscellaneousItem_edit, name='MiscellaneousItem_edit'),
    path('Medicine', Medicine_list, name='Medicine_list'),
    path('Medicine/<int:passed_id>', Medicine_edit, name='Medicine_edit'),

    #doctor url

    path('diagnosis_list',diagnosis_list),
    path('diagnosis_info/<int:passed_id>',diagnosis_info),
    path('testPrescribed_list',testPrescribed_list),
    path('testPrescribed_info/<int:passed_id>',testPrescribed_info),
    path('medPrescribed_list',medPrescribed_list),
    path('medPrescribed_info/<int:passed_id>',medPrescribed_info),
    path('list_of_test',list_of_test),
    path('list_of_medicine',list_of_medicine),
    path('Medicine/<int:passed_id>', Medicine_edit, name='Medicine_edit'),
    path('generate_miscellaneousitem_report/', generate_miscellaneousitem_report, name='generate_miscellaneousitem_report'),
    path('generate_supplier_report/', generate_supplier_report, name='generate_supplier_report'),
    path('generate_equipment_report/', generate_equipment_report, name='generate_equipment_report'),
    path('generate_order_report/', generate_order_report, name='generate_order_report'),
    path('generate_medicine_report/', generate_medicine_report, name='generate_medicine_report'),
    path('get_report', get_report, name='get_report'),
    # path('export_report_csv/<int:report_id>/', export_report_csv, name='export_report_csv'),
    path('test_list', list_of_test),
    path('test_list/<int:passed_id>',testing_edit),
    path('live',live),
    path('details_list', list_of_values),
    path('list_of_values1', list_of_values1),
    path('details_list/<int:passed_id>', values_edit),
    path('search_test/<str:search_test>',search_test),
    path('diagnosis_list',diagnosis_list),
    path('diagnosis_info/<int:passed_id>',diagnosis_info),
    path('testPrescribed_list',testPrescribed_list),
    path('testPrescribed_info/<int:passed_id>',testPrescribed_info),
    path('isactivetruelist',testPrescribed_isactivetruelist),
    path('isactivefalselist',testPrescribed_isactivefalselist),
    path('isactivetrue/<int:passed_id>',testPrescribed_isactivetrue),
    path('isactivefalse/<int:passed_id>',testPrescribed_isactivefalse),
    #receptionist
    path('patient_list',patient_list),
    path('patient_info/<int:passed_id>',patient_info),
    path('search_patient/<int:search_Patient>',search_patient),
    path('search_info/<str:search_Patient>',search_patient),
    path('appointment_list',appointment_list),
    path('appointment_info/<int:passed_id>',appointment_info),
    path('search_appointment/<str:search_appoint>',search_appointment),
    #doctor
    path('doctor_test',testPrescribed_list)

    path('changepassword/',ChangePassword.as_view()),
     path('appointment_list', AppointmentListView.as_view()),
    path('diagnosis_list',diagnosis_list),
    path('diagnosis_info/<int:passed_id>',diagnosis_info),
    path('medPrescribed_list',medPrescribed_list),
    path('medPrescribed_info/<int:passed_id>',medPrescribed_info),
    path('pharmacist',pharmacist_data),
    path('pharma_bill/<int:pharmacist_id>',generate_bill)
]
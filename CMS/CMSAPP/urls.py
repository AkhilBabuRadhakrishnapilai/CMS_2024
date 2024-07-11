from django.urls import path
from .views import *

urlpatterns = [
    path('addemployee/',EmployeeCRUD.as_view()),
    path('employeelist/',EmployeeCRUD.as_view()),
    path('edit/<str:emp_id>',EmployeeCRUD.as_view()),
    path('disable/<str:emp_id>',EmployeeCRUD.as_view()),
    path('login',Login.as_view()),
    #stock_management urls
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
       path('generate_miscellaneousitem_report/', generate_miscellaneousitem_report, name='generate_miscellaneousitem_report'),
   path('generate_supplier_report/', generate_supplier_report, name='generate_supplier_report'),
   path('generate_equipment_report/', generate_equipment_report, name='generate_equipment_report'),
    path('generate_order_report/', generate_order_report, name='generate_order_report'),
    path('generate_medicine_report/', generate_medicine_report, name='generate_medicine_report'),
    path('get_report', get_report, name='get_report'),
    # path('export_report_csv/<int:report_id>/', export_report_csv, name='export_report_csv'),
]
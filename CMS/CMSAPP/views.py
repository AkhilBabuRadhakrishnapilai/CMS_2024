from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import JsonResponse,HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
# Create your views here.

#admin
#login
class Login(APIView):
    def post(self,request):
        employee = LoginSerializer(data=request.data)
        if employee.is_valid:
            email = employee.validated_data["email"]
            password = employee.validated_data["password"]
            print(email)
            auth_user = authenticate(request,email=email,password=password)
            if auth_user is not None:
                token = Token.objects.get(user=auth_user)
                #for getting the user as an object
                user_data = UserSerializer(auth_user).data
                response ={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "data":{
                        "Token":token.key,
                        "user":user_data
                    }
                }
                return Response (response,status = status.HTTP_200_OK)
            else:
                response = {
                     "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"Invalid Username or password",
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = {
                "status":status.HTTP_400_BAD_REQUEST,
                "message":"Bad Request"
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

#employee management
class EmployeeCRUD(APIView):
    
    def get(self,request):
        employee_db = User.objects.all()
        employee = UserSerializer(employee_db,many=True)
        return JsonResponse(employee.data,status = 200,safe=False)
    
    def post(self,request):
        employee = UserSerializer(data=request.data)
        if employee.is_valid():
            employee.save()
            return HttpResponse(employee.data,status = 200)
        return HttpResponse(employee.errors,status = 400)
    
    def put(self,request,emp_id):
        try:
            employee_db = User.objects.get(pk=emp_id)
        except User.DoesNotExist:
            return JsonResponse({"error":"Employee not Found"},status = 404)
        employee = UserSerializer(employee_db,data=request.data,partial=True)
        if employee.is_valid():
            employee.save()
            return HttpResponse(employee.data,status=200)
        return HttpResponse(employee.errors,status = 400)
    
    def delete(self,request,emp_id):
        employee_db = User.objects.get(pk= emp_id)
        employee_db.is_active = False
        employee_db.save()
        return JsonResponse({"message": "Employee deleted successfully"}, status= status.HTTP_204_NO_CONTENT)
    
    

#approvals
class AdminApproval(APIView):
    pass





# view of supplier model for get and post
@api_view(['GET', 'POST'])
def supplier_list(request):
    if request.method == 'GET':
        suppliers = Supplier.objects.filter(is_active=True)
        suppliers_serializer = SupplierSerializer(suppliers, many=True)
        return JsonResponse(suppliers_serializer.data, safe=False)

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        supplier_serializer = SupplierSerializer(data=request_data)
        if supplier_serializer.is_valid():
            supplier_serializer.save()
            return JsonResponse(supplier_serializer.data, status=201)
        return JsonResponse(supplier_serializer.errors, status=400)

# view of stock_management   

# view of supplier model for get,put,delete
@api_view(['GET','PUT','DELETE'])

def supplier_edit(request, passed_id):
    try:
        supplier_details = Supplier.objects.get(id=passed_id)
    except Supplier.DoesNotExist:
        return JsonResponse({'error': 'Supplier not found'}, status=404)

    if request.method == 'GET':
        supplier_serializer = SupplierSerializer(supplier_details)
        return JsonResponse(supplier_serializer.data)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        supplier_update_serializer = SupplierSerializer(supplier_details, data=request_data)
        if supplier_update_serializer.is_valid():
            supplier_update_serializer.save()
            return JsonResponse(supplier_update_serializer.data, status=200)
        return JsonResponse(supplier_update_serializer.errors, status=400)
    elif request.method == 'DELETE':
        supplier_details.is_active = False  # Soft delete by setting is_active to False
        supplier_details.save()
        return JsonResponse({'message': 'Supplier deactivated successfully'}, status=204)
    
# view of order model for get and post
@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(is_active=True)
        order_serializer = OrderSerializer(orders, many=True)
        return JsonResponse(order_serializer.data, safe=False)

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        order_serializer = OrderSerializer(data=request_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse(order_serializer.data, status=201)
        return JsonResponse(order_serializer.errors, status=400)


# view of order model for get,put,delete
@api_view(['GET','PUT','DELETE'])


def order_edit(request, passed_id):
    try:
        order_details = Order.objects.get(id=passed_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == 'GET':
        order_serializer = OrderSerializer(order_details)
        return JsonResponse(order_serializer.data)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        oder_update_serializer = OrderSerializer(order_details, data=request_data)
        if oder_update_serializer.is_valid():
            oder_update_serializer.save()
            return JsonResponse(oder_update_serializer.data, status=200)
        return JsonResponse(oder_update_serializer.errors, status=400)
    elif request.method == 'DELETE':
        order_details.is_active = False  # Soft delete by setting is_active to False
        order_details.save()
        return JsonResponse({'message': 'order deactivated successfully'}, status=204)


@api_view(['GET', 'POST'])
def equipment_list(request):
    if request.method == 'GET':
        equipment = Equipment.objects.filter(is_active=True)
        equipment_serializer = EquipmentSerializer(equipment, many=True)
        return JsonResponse(equipment_serializer.data, safe=False)

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        equipment_serializer = EquipmentSerializer(data=request_data)
        if equipment_serializer.is_valid():
            equipment_serializer.save()
            return JsonResponse(equipment_serializer.data, status=201)
        return JsonResponse(equipment_serializer.errors, status=400)


@api_view(['GET','PUT','DELETE'])


def equipment_edit(request, passed_id):
    try:
        equipment_details = Equipment.objects.get(id=passed_id)
    except Equipment.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if request.method == 'GET':
        equipment_serializer = EquipmentSerializer(equipment_details)
        return JsonResponse(equipment_serializer.data)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        equipment_update_serializer = EquipmentSerializer(equipment_details, data=request_data)
        if equipment_update_serializer.is_valid():
            equipment_update_serializer.save()
            return JsonResponse(equipment_update_serializer.data, status=200)
        return JsonResponse(equipment_update_serializer.errors, status=400)
    elif request.method == 'DELETE':
        equipment_details.is_active = False  # Soft delete by setting is_active to False
        equipment_details.save()
        return JsonResponse({'message': 'order deactivated successfully'}, status=204)
    
@api_view(['GET', 'POST'])
def MiscellaneousItem_list(request):
    if request.method == 'GET':
        miscellaneousItem = MiscellaneousItem.objects.filter(is_active=True)
        MiscellaneousItem_serializer = MiscellaneousItemSerializer(miscellaneousItem, many=True)
        return JsonResponse(MiscellaneousItem_serializer.data, safe=False)

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        MiscellaneousItem_serializer = MiscellaneousItemSerializer(data=request_data)
        if MiscellaneousItem_serializer.is_valid():
            MiscellaneousItem_serializer.save()
            return JsonResponse(MiscellaneousItem_serializer.data, status=201)
        return JsonResponse(MiscellaneousItem_serializer.errors, status=400)


@api_view(['GET','PUT','DELETE'])


def MiscellaneousItem_edit(request, passed_id):
    try:
        MiscellaneousItem_details = MiscellaneousItem.objects.get(id=passed_id)
    except MiscellaneousItem.DoesNotExist:
        return JsonResponse({'error': 'MiscellaneousItem not found'}, status=404)

    if request.method == 'GET':
        MiscellaneousItem_serializer = MiscellaneousItemSerializer(MiscellaneousItem_details)
        return JsonResponse(MiscellaneousItem_serializer.data)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        MiscellaneousItem_update_serializer = MiscellaneousItemSerializer(MiscellaneousItem_details, data=request_data)
        if MiscellaneousItem_update_serializer.is_valid():
            MiscellaneousItem_update_serializer.save()
            return JsonResponse(MiscellaneousItem_update_serializer.data, status=200)
        return JsonResponse(MiscellaneousItem_update_serializer.errors, status=400)
    elif request.method == 'DELETE':
        MiscellaneousItem_details.is_active = False  # Soft delete by setting is_active to False
        MiscellaneousItem_details.save()
        return JsonResponse({'message': 'MiscellaneousItem deactivated successfully'}, status=204)
    
@api_view(['GET', 'POST'])
def Medicine_list(request):
    if request.method == 'GET':
        medicineItem = Medicine.objects.filter(is_active=True)
        MedicineItem_serializer = MedSerializer(medicineItem, many=True)
        return JsonResponse(MedicineItem_serializer.data, safe=False)

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        MedicineItem_serializer = MedSerializer(data=request_data)
        if MedicineItem_serializer.is_valid():
            MedicineItem_serializer.save()
            return JsonResponse(MedicineItem_serializer.data, status=201)
        return JsonResponse(MedicineItem_serializer.errors, status=400)


@api_view(['GET','PUT','DELETE'])


def Medicine_edit(request, passed_id):
    print("mmmm")
    try:
        print("hey")
        print(passed_id)
        Medicine_details = Medicine.objects.get(id=passed_id)
        
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found'}, status=404)

    if request.method == 'GET':
        Medicine_serializer = MedSerializer(Medicine_details)
        return JsonResponse(Medicine_serializer.data)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        Medicine_update_serializer = MedSerializer(Medicine_details, data=request_data)
        if Medicine_update_serializer.is_valid():
            Medicine_update_serializer.save()
            return JsonResponse(Medicine_update_serializer.data, status=200)
        return JsonResponse(Medicine_update_serializer.errors, status=400)
    elif request.method == 'DELETE':
        Medicine_details.is_active = False  # Soft delete by setting is_active to False
        Medicine_details.save()
        return JsonResponse({'message': 'Medicine deactivated successfully'}, status=204)

@api_view(['GET'])
def generate_supplier_report(request):
    suppliers = Supplier.objects.filter(is_active=True)
    supplier_data = SupplierSerializer(suppliers, many=True).data
    report = Report.objects.create(
        report_type='SUPPLIER',
        data=json.dumps(supplier_data)
    )
    return JsonResponse(ReportSerializer(report).data, status=201)

@api_view(['GET'])
def generate_order_report(request):
    orders = Order.objects.filter(is_active=True)
    order_data = OrderSerializer(orders, many=True).data
    report = Report.objects.create(
        report_type='ORDER',
        data=json.dumps(order_data)
    )
    return JsonResponse(ReportSerializer(report).data, status=201)

@api_view(['GET'])
def generate_medicine_report(request):
    medicines = Medicine.objects.filter(is_active=True)
    medicine_data = MedSerializer(medicines, many=True).data
    report = Report.objects.create(
        report_type='MEDICINE',
        data=json.dumps(medicine_data)
    )
    return JsonResponse(ReportSerializer(report).data, status=201)
@api_view(['GET'])
def generate_equipment_report(request):
    equipment = Equipment.objects.filter(is_active=True)
    equipment_data = EquipmentSerializer(equipment, many=True).data
    report = Report.objects.create(
        report_type='EQUIPMENT',
        data=json.dumps(equipment_data)
    )
    return JsonResponse(ReportSerializer(report).data, status=201)
@api_view(['GET'])
def generate_miscellaneousitem_report(request):
    miscellaneousitem = MiscellaneousItem.objects.filter(is_active=True)
    miscellaneousitem_data = MiscellaneousItemSerializer(miscellaneousitem, many=True).data
    report = Report.objects.create(
        report_type='MISCELLANEOUSITEM',
        data=json.dumps(miscellaneousitem_data)
    )
    return JsonResponse(ReportSerializer(report).data, status=201)

@api_view(['GET'])
def get_report(request):
   
        report = Report.objects.all()
        report_serializer = ReportSerializer(report, many=True)
        return JsonResponse(report_serializer.data, safe=False)



# @api_view(['GET'])
# def export_report_csv(request, report_id):
#     try:
#         report = Report.objects.get(id=report_id)
#     except Report.DoesNotExist:
#         return JsonResponse({'error': 'Report not found'}, status=404)
    
#     report_data = json.loads(report.data)
#     print("Report Data:", report_data)  # Debug output to see the structure of report_data

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename="{report.get_report_type_display()}_{report.generated_at}.csv"'

#     writer = csv.writer(response)
    
#     if report.report_type == 'SUPPLIER':
#         writer.writerow(['ID', 'Name', 'Address', 'Phone', 'Email', 'Is Active'])
#         for item in report_data:
#             writer.writerow([
#                 item['id'], 
#                 item['name'], 
#                 item['address'], 
#                 item['phone'], 
#                 item['email'], 
#                 item['is_active']
#             ])
    
#     elif report.report_type == 'ORDER':
#         writer.writerow(['ID', 'Supplier ID', 'Order Date', 'Expected Delivery Date', 'Status', 'Supplier Name', 'Supplier Address', 'Supplier Phone', 'Supplier Email'])
#         for item in report_data:
#             supplier = item['suppliee']
#             writer.writerow([
#                 item['id'], 
#                 item['supplier'], 
#                 item['order_date'], 
#                 item['expected_delivery_date'], 
#                 item['status'], 
#                 supplier['name'],
#                 supplier['address'],
#                 supplier['phone'],
#                 supplier['email'],
#             ])
    
#     elif report.report_type == 'MEDICINE':
#         writer.writerow(['ID', 'Name', 'Generic Name', 'Category', 'Type', 'Description', 'Storage Requirements', 'Stock', 'Unit Price', 'Date Created', 'Expiry Date', 'Reorder Level', 'Supplier ID', 'Supplier Name', 'Supplier Address', 'Supplier Phone', 'Supplier Email'])
#         for item in report_data:
#             supplier = item['suppliee']
#             writer.writerow([
#                 item['id'], 
#                 item['name'], 
#                 item['generic_name'], 
#                 item['category'], 
#                 item['type_medicine'], 
#                 item['description'], 
#                 item['storage_requirements'], 
#                 item['stock'], 
#                 item['unit_price'], 
#                 item['date_created'], 
#                 item['expiry_date'], 
#                 item['reorder_level'], 
#                 item['supplier'], 
#                 supplier['name'],
#                 supplier['address'],
#                 supplier['phone'],
#                 supplier['email'],
#             ])
    
#     return response


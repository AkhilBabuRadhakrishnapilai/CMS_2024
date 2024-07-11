from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import JsonResponse,HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django.db.models import Q
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
        if employee.is_valid():
            email = employee.validated_data["email"]
            password = employee.validated_data["password"]
            auth_user = authenticate(request,email=email,password=password)
            if auth_user is not None:
                token = Token.objects.get(user=auth_user)
                #for getting the user as an object
                user_data = UserSerializer(auth_user).data
                print("hey hey")
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
        employee_db = User.objects.filter(is_active=True)
        employee = UserSerializer(employee_db,many=True)
        return JsonResponse(employee.data,status = 200,safe=False)

    def post(self,request):
        role_id = request.data.get('role_id')
        employee_ser = UserSerializer(data=request.data)
        
        if employee_ser.is_valid():
            employee = employee_ser.save()
            print(role_id)
            print(type(role_id))
            if role_id == "3":
                print("1st here")
                doctor_data = {
                    'user_id': employee.emp_id,
                    'specialization': request.data.get('specialization_id'),
                    'fees': request.data.get('fees', 0)
                }
                print("2nd here")
                print(doctor_data)
                doctor = DoctorsSerializer(data=doctor_data)
                if doctor.is_valid():
                    doctor.save()
                    return JsonResponse(doctor.data, status=201, safe=False)
                else:
                    employee.delete()
                    return HttpResponse(doctor.errors, status=400)
            return JsonResponse(employee_ser.data, status=201, safe=False)
        return HttpResponse(employee_ser.errors, status=400)
            
    def put(self,request,emp_id):
        try:
            employee_db = User.objects.get(pk=emp_id)
        except User.DoesNotExist:
            return JsonResponse({"error":"Employee not Found"},status = 404)
        employee = UserSerializer(employee_db,data=request.data,partial=True)
        if employee.is_valid():
            emp=employee.save()
            if emp.role.id == "3":
                print(emp_id)
                try: 
                    doc = Doctors.objects.get(user_id=emp_id)
                except Doctors.DoesNotExist:
                    return JsonResponse({'error':"Doctor Not Found"},status=400)
                doc_data={
                    'specialization': request.data.get('specialization_id'),
                    'fees': request.data.get('fees', 0)
                }
                print("edit done")
                doc_ser=DoctorsSerializer(doc,data=doc_data,partial=True)
                if doc_ser.is_valid():
                    doc_ser.save()
                    return JsonResponse(doc_ser.data,status=200)
                return JsonResponse(doc_ser.errors,status=400)
            return JsonResponse(employee.data,status=200)
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

    
#qualification
class GetAllQualifications(APIView):
    def get(self,request):
        qualification_db = Qualification.objects.all()
        qualifications = QualificationSerializer(qualification_db,many=True)
        return JsonResponse(qualifications.data,status=200,safe=False)
    
#specialization
class GetAllSpecializations(APIView):
    def get(self,request):
        specialization_db = Specialization.objects.all()
        specialization = SpecializationSerializer(specialization_db,many=True)
        return JsonResponse(specialization.data,status=200,safe=False)
    
#gender
class GetAllGenders(APIView):
    def get(self,request):
        gender_db = Gender.objects.all()
        gender = GenderSerializer(gender_db,many=True)
        return JsonResponse(gender.data,status=200,safe=False)
    
#role
class GetAllRoles(APIView):
    def get(self,request):
        try:
            roles_db = Roles.objects.all()
            roles = RolesSerializer(roles_db,many=True)
            return JsonResponse(roles.data,status=200,safe=False)
        except:
            return HttpResponse(roles.error_messages,status=400)

class ChangePassword(APIView):
    def patch(self,request,email):
        try:
            user_db = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"employee not found"},status=400)
        password = request.data.get('password')
        if password:
            user_db.password = make_password(password)
            user_db.save()
            return JsonResponse(user_db.data,status=200)
        return HttpResponse(user_db.errors,status=400)

# receptionist views
# for listing all the patients
class PatientListView(APIView):    
    permission_classes = [AllowAny]
    # method = GET
    def get(self, request):
        patient_list = patient_details.objects.all()
        patient_list_serializer = PatientDetailsSerializer(patient_list, many=True)
        return JsonResponse(patient_list_serializer.data, safe=False)
    # method = POST
    def post(self, request):
        request_data = JSONParser().parse(request)
        patient_add_serializer = PatientDetailsSerializer(data=request_data)
        if patient_add_serializer.is_valid():
            patient_add_serializer.save()
            return JsonResponse(patient_add_serializer.data, status=201)
        return JsonResponse(patient_add_serializer.errors, status=400)

# for editing, deleting patients
class PatientInfoView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, passed_id):
        try:
            return patient_details.objects.get(pk=passed_id, is_active=True)
        except patient_details.DoesNotExist:
            return None

    def get(self, request, passed_id):
        patient_info = self.get_object(passed_id)
        if not patient_info:
            return HttpResponse(status=404)
        patient_info_serializer = PatientDetailsSerializer(patient_info)
        return JsonResponse(patient_info_serializer.data, safe=False)

    def put(self, request, passed_id):
        patient_info = self.get_object(passed_id)
        if not patient_info:
            return HttpResponse(status=404)

        try:
            request_data = JSONParser().parse(request)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        patient_update_serializer = PatientDetailsSerializer(patient_info, data=request_data, partial=True)
        if patient_update_serializer.is_valid():
            patient_update_serializer.save()
            return JsonResponse(patient_update_serializer.data, status=200)
        return JsonResponse(patient_update_serializer.errors, status=400)

    def delete(self, request, passed_id):
        patient_info = self.get_object(passed_id)
        if not patient_info:
            return HttpResponse(status=404)
        patient_info.is_active = False
        patient_info.save
        return HttpResponse(status=204)


class SearchPatientView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, search_patient):
        patients = patient_details.objects.filter(
            Q(opid__icontains=search_patient) | 
            Q(name__icontains=search_patient) | 
            Q(mobile__icontains=search_patient)
        )
        patient_serializer = PatientDetailsSerializer(patients, many=True)
        return JsonResponse(patient_serializer.data, safe=False)


class AppointmentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        appoint_list = BookAppointment.objects.all()
        appoint_list_serializer = BookAppointmentSerializer(appoint_list, many=True)
        return JsonResponse(appoint_list_serializer.data, safe=False)

    def post(self, request):
        request_data = JSONParser().parse(request)
        appoint_add_serializer = BookAppointmentSerializer(data=request_data)
        if appoint_add_serializer.is_valid():
            appoint_add_serializer.save()
            return JsonResponse(appoint_add_serializer.data, status=201)
        return JsonResponse(appoint_add_serializer.errors, status=400)


class AppointmentInfoView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, passed_id):
        try:
            return BookAppointment.objects.get(id=passed_id)
        except BookAppointment.DoesNotExist:
            return None

    def get(self, request, passed_id):
        appoint_info = self.get_object(passed_id)
        if not appoint_info:
            return HttpResponse(status=404)
        appoint_serializer = BookAppointmentSerializer(appoint_info)
        return JsonResponse(appoint_serializer.data, safe=False)

    def put(self, request, passed_id):
        appoint_info = self.get_object(passed_id)
        if not appoint_info:
            return HttpResponse(status=404)
        request_data = JSONParser().parse(request)
        appoint_update_serializer = BookAppointmentSerializer(appoint_info, data=request_data)
        if appoint_update_serializer.is_valid():
            appoint_update_serializer.save()
            return JsonResponse(appoint_update_serializer.data, status=200)
        return JsonResponse(appoint_update_serializer.errors, status=400)

    def delete(self, request, passed_id):
        appoint_info = self.get_object(passed_id)
        if not appoint_info:
            return HttpResponse(status=404)
        appoint_info.delete()
        return HttpResponse(status=204)


class SearchAppointmentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, search_appoint):
        appoint = BookAppointment.objects.filter(doctor__icontains=search_appoint)
        appoint_serializer = BookAppointmentSerializer(appoint, many=True)
        return JsonResponse(appoint_serializer.data, safe=False)

class SpecializationList(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request):
        specs = Specialization.objects.all()
        spec_serializer = SpecializationSerializer(specs, many=True)
        return JsonResponse(spec_serializer.data, safe=False)

class DoctorList(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request):
        doc = Doctors.objects.all()
        doc_serializer = DoctorsSerializer(doc, many=True)
        return JsonResponse(doc_serializer.data,safe=False)

class GetToken(APIView):
    def get(self,request):
        token = generate_token()
        return JsonResponse({'token': token})


class GetOp(APIView):
    def get(self, request, opid):
        opid = patient_details.objects.filter(opid=opid)
        op_serializer = PatientDetailsSerializer(opid, many=True)
        return JsonResponse(op_serializer.data, safe=False)

#Doctor views

@csrf_exempt
@api_view(['GET', 'POST'])
def list_of_test(request):
    if request.method == "GET":
        testing = NewTest.objects.all()
        testing_serialize = NewTest_Serializer(testing, many=True)
        return JsonResponse(testing_serialize.data, safe=False)
    
@csrf_exempt
@api_view(['GET', 'POST'])
def list_of_medicine(request):
    if request.method == "GET":
        medicine_test = Medicine.objects.all()
        med_testing_serialize = Medicine_Serializer(medicine_test, many=True)
        return JsonResponse(med_testing_serialize.data, safe=False)

@csrf_exempt
@api_view(['GET','POST'])
def diagnosis_list(request):
    if request.method == 'GET':
        diagnosis_list = Diagnosis.objects.all()
        diagnosis_list_serializer = DiagnosisSerializer(diagnosis_list, many=True)
        return JsonResponse(diagnosis_list_serializer.data, safe=False)

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        diagnosis_add_serializer = DiagnosisSerializer(data=request_data)
        if diagnosis_add_serializer.is_valid():
            diagnosis_add_serializer.save()
            return JsonResponse(diagnosis_add_serializer.data, status=201)
        return JsonResponse(diagnosis_add_serializer.errors, status=400)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def diagnosis_info(request, passed_id):
    try:
        diagnosis_info = Diagnosis.objects.get(id=passed_id)
    except Diagnosis.DoesNotExist:
        return JsonResponse({'error': 'Diagnosis not found'}, status=404)

    if request.method == 'GET':
        diagnosis_serializer = DiagnosisSerializer(diagnosis_info)
        return JsonResponse(diagnosis_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        diagnosis_update_serializer = DiagnosisSerializer(diagnosis_info, data=request_data)
        if diagnosis_update_serializer.is_valid():
            diagnosis_update_serializer.save()
            return JsonResponse(diagnosis_update_serializer.data, status=200)
        return JsonResponse(diagnosis_update_serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        diagnosis_info.delete()
        return HttpResponse(status=204)

@csrf_exempt
@api_view(['GET','POST'])
def testPrescribed_list(request):
    if request.method == 'GET':
        testPrescribed_list = TestPrescribed.objects.all()
        test_prescribed_serializer = TestPrescribedSerializer(testPrescribed_list, many=True)
        return JsonResponse(test_prescribed_serializer.data, safe=False)
    
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        test_prescribed_add_serializer = TestPrescribedSerializer(data=request_data)
        if test_prescribed_add_serializer.is_valid():
            test_prescribed_add_serializer.save()
            return JsonResponse(test_prescribed_add_serializer.data, status=201)
        return JsonResponse(test_prescribed_add_serializer.errors, status=400)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def testPrescribed_info(request, passed_id):
    try:
        test_info = TestPrescribed.objects.get(id=passed_id)
    except TestPrescribed.DoesNotExist:
        return JsonResponse({'error': 'TestPrescribed not found'}, status=404)

    if request.method == 'GET':
        test_serializer = TestPrescribedSerializer(test_info)
        return JsonResponse(test_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        test_update_serializer = TestPrescribedSerializer(test_info, data=request_data)
        if test_update_serializer.is_valid():
            test_update_serializer.save()
            return JsonResponse(test_update_serializer.data, status=200)
        return JsonResponse(test_update_serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        test_info.delete()
        return HttpResponse(status=204)



@csrf_exempt
@api_view(['GET','POST'])
def medPrescribed_list(request):
    if request.method == 'GET':
        medPrescribed_list = MedPrescribed.objects.all()
        med_prescribed_serializer = MedPrescribedSerializer(medPrescribed_list, many=True)
        return JsonResponse(med_prescribed_serializer.data,safe=False)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        med_prescribed_add_serializer = MedPrescribedSerializer(data=request_data)
        if med_prescribed_add_serializer.is_valid():
            med_prescribed_add_serializer.save()
            return JsonResponse(med_prescribed_add_serializer.data, status=201)
        return JsonResponse(med_prescribed_add_serializer.errors,status=400)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def medPrescribed_info(request, passed_id):
    try:
        med_info = MedPrescribed.objects.get(id=passed_id)
    except MedPrescribed.DoesNotExist:
        return JsonResponse({'error': 'MedPrescribed not found'}, status=404)

    if request.method == 'GET':
        med_serializer = MedPrescribedSerializer(med_info)
        return JsonResponse(med_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        med_update_serializer = MedPrescribedSerializer(med_info, data=request_data)
        if med_update_serializer.is_valid():
            med_update_serializer.save()
            return JsonResponse(med_update_serializer.data, status=200)
        return JsonResponse(med_update_serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        med_info.delete()
        return HttpResponse(status=204)
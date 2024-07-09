from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import JsonResponse,HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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


#Doctor_views

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
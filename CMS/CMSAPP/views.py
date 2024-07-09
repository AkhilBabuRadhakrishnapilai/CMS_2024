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
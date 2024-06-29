from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.http import JsonResponse,HttpResponse
# Create your views here.

#admin
#signin
#login
#add employee
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

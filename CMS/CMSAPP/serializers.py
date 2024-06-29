from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.Serializer):
    class Meta:
        model= Department
        fields = '__all__'

class QualificationSerializer(serializers.Serializer):
    department = DepartmentSerializer()
    class Meta:
        model = Qualification
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    department = DepartmentSerializer()
    qualification = QualificationSerializer()
    class Meta:
        model = User
        fields = '__all__'

class SpecializationSerializer(serializers.Serializer):
    dept = DepartmentSerializer()
    class Meta:
        model = Specialization
        fields = '__all__'

class DoctorsSerializer(serializers.Serializer):
    user_id = UserSerializer()
    specialization = SpecializationSerializer()
    class Meta:
        model = Doctors
        fields = '__all__'
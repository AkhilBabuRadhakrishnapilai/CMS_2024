from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Department
        fields = '__all__'

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    qualification = serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all())
    specialization = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all())
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        department = validated_data.pop('department')
        qualification = validated_data.pop('qualification')
        specialization = validated_data.pop('specialization')
        gender = validated_data.pop('gender')
        role = validated_data.pop('role')
        #for hasing the password
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        user = User.objects.create(
            department=department,
            qualification=qualification,
            specialization=specialization,
            gender=gender,
            role=role,
            **validated_data
        )

        return user
    
    def update(self,instance,validated_data):
        department_data = validated_data.pop('department')
        qualification_data = validated_data.pop('qualification')
        specialization_data = validated_data.pop('specialization')
        gender_data = validated_data.pop('gender')
        role_data = validated_data.pop('role')
        #for hasing the password
        password = validated_data.pop('password')
        if password:
            hashed_password = make_password(password)
            instance.password = hashed_password

        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.address = validated_data.get('address',instance.address)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.date_of_joining = validated_data.get('date_of_joining',instance.date_of_joining)

        #updatng the related fields
        if isinstance(department_data, dict):
            department, created = Department.objects.get_or_create(**department_data)
            instance.department = department
        if isinstance(qualification_data, dict):
            qualification, created = Qualification.objects.get_or_create(**qualification_data)
            instance.qualification = qualification
        if isinstance(specialization_data, dict):
            specialization, created = Specialization.objects.get_or_create(**specialization_data)
            instance.specialization = specialization
        if isinstance(gender_data, dict):
            gender, created = Gender.objects.get_or_create(**gender_data)
            instance.gender = gender
        if isinstance(role_data, dict):
            role, created = Roles.objects.get_or_create(**role_data)
            instance.role = role
        
        instance.save()

        return instance
        

class DoctorsSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    specialization = SpecializationSerializer()
    class Meta:
        model = Doctors
        fields = '__all__'

#login
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password']
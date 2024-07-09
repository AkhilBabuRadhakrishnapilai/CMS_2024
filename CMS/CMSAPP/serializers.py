from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Department
#         fields = '__all__'

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

class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

    #qualification
    qualification = QualificationSerializer(read_only = True)
    qualification_id = serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all())
    #Gender
    gender = GenderSerializer(read_only=True)
    gender_id = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all())
    #role
    role = RolesSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all())

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        qualification = validated_data.pop('qualification_id')
        gender = validated_data.pop('gender_id')
        role = validated_data.pop('role_id')

        user = User.objects.create(
            **validated_data
        )

        print("2nd here")
        user.qualification = qualification
        user.gender = gender
        user.role = role

        user.save()

        return user
    
    def update(self,instance,validated_data):
        qualification_data = validated_data.pop('qualification_id')
        gender_data = validated_data.pop('gender_id')
        role_data = validated_data.pop('role_id')
        #for hasing the password
        # password = validated_data.pop('password')
        # if password:
        #     hashed_password = make_password(password)
        #     instance.password = hashed_password

        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.address = validated_data.get('address',instance.address)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.date_of_joining = validated_data.get('date_of_joining',instance.date_of_joining)
        instance.contact_number = validated_data.get('contact_number',instance.contact_number)

        #updatng the related fields
        if isinstance(qualification_data, dict):
            qualification, created = Qualification.objects.get_or_create(**qualification_data)
            instance.qualification = qualification
        if isinstance(gender_data, dict):
            gender, created = Gender.objects.get_or_create(**gender_data)
            instance.gender = gender
        if isinstance(role_data, dict):
            role, created = Roles.objects.get_or_create(**role_data)
            instance.role = role
        
        instance.save()
        return instance

    
#login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password= serializers.CharField(max_length=128,write_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['email','password','role']
        
# receptionist serializers
class PatientDetailsSerializer(serializers.ModelSerializer):
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all())
    class Meta:
        model = patient_details
        fields = '__all__'

class BookAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=patient_details.objects.all())
    specialization = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctors.objects.all())

    class Meta:
        model = BookAppointment
        fields = '__all__'

    def create(self, validated_data):
        return BookAppointment.objects.create(**validated_data)
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['patient'] = PatientDetailsSerializer(instance.patient).data  # Serialize patient details separately if needed
        rep['specialization'] = SpecializationSerializer(instance.specialization).data
        rep['doctor'] = DoctorsSerializer(instance.doctor).data
        return rep

    def update(self, instance, validated_data):
        instance.patient = validated_data.get('patient', instance.patient)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.doctor = validated_data.get('doctor', instance.doctor)
        instance.appointment_date = validated_data.get('appointment_date', instance.appointment_date)
        instance.time_slot = validated_data.get('time_slot', instance.time_slot)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
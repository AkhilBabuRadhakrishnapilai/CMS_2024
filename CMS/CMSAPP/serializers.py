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

class DoctorsSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = Doctors
        fields = '__all__'

class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient_details
        fields = '__all__'

#login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password= serializers.CharField(max_length=128,write_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['email','password','role']
class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient_details
        fields = '__all__'

class BookAppointmentSerializer(serializers.ModelSerializer):
    patient = PatientDetailSerializer(read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    doctor = DoctorsSerializer(read_only=True)

    class Meta:
        model = BookAppointment
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    appointment = serializers.PrimaryKeyRelatedField(queryset=BookAppointment.objects.all())
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = '__all__'

    def create(self, validated_data):
        # Directly use the appointment instance
        diagnosis = Diagnosis.objects.create(**validated_data)
        return diagnosis

    def update(self, instance, validated_data):
        appointment_data = validated_data.pop('appointment', None)
        if appointment_data:
            instance.appointment = appointment_data
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_patient(self, obj):
        return PatientDetailSerializer(obj.appointment.patient).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['appointment'] = BookAppointmentSerializer(instance.appointment).data
        representation['patient'] = representation['appointment']['patient']  # Directly assign patient from appointment
        return representation
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '_all_'

class MedSerializer(serializers.ModelSerializer):
    suppliee=SupplierSerializer(read_only=True)
    class Meta:
        model = Medicine
        fields = ('id','name','generic_name','category','type_medicine',
                  'description','storage_requirements','stock','unit_price',
                  'date_created','expiry_date','reorder_level','supplier','suppliee')
    def create(self, validated_data):
        supplier = validated_data.pop('supplier', None)
        order = (Medicine.objects.create(**validated_data,supplier=supplier))
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['suppliee'] = SupplierSerializer(instance.supplier).data

        return rep
class MedPrescribedSerializer(serializers.ModelSerializer):
    med = serializers.PrimaryKeyRelatedField(queryset=Diagnosis.objects.all())
    patient = serializers.SerializerMethodField()
    med_list = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all(), many=True, write_only=True)
    med_list_details = MedSerializer(many=True, read_only=True, source='med_list')

    class Meta:
        model = MedPrescribed
        fields = '__all__'

    def create(self, validated_data):
        med_list_data = validated_data.pop('med_list')
        med_prescribed = MedPrescribed.objects.create(**validated_data)
        med_prescribed.med_list.set(med_list_data)
        return med_prescribed
    
    def update(self, instance, validated_data):
        med_list_data = validated_data.pop('med_list', None)
        if med_list_data:
            instance.med_list.set(med_list_data)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def get_patient(self, obj):
        return PatientDetailSerializer(obj.med.appointment.patient).data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['med'] = DiagnosisSerializer(instance.med).data
        representation['patient'] = representation['med']['appointment']['patient']
        representation['med_list'] = MedSerializer(instance.med_list.all(), many=True).data
        return representation



class PharmacistSerializer(serializers.ModelSerializer):
    opid = serializers.CharField(source='opid.patient.opid', read_only=True)
    doctor = serializers.CharField(source='doctor.doctor.user_id.first_name', read_only=True)
    medicines = serializers.SerializerMethodField()
    # total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Pharmacist
        fields = '__all__'

    def get_medicines(self, obj):
        medicines_list = []
        prescriptions = obj.medicines.all()
        for prescription in prescriptions:
            for medicine in prescription.med_list.all():  # Use .all() to fetch related medicines
                medicines_list.append({
                    'medicine_name': medicine.name,
                    'unit_price': medicine.unit_price,
                    'total_price': medicine.unit_price * (prescription.morning + prescription.noon + prescription.night),
                })
        return medicines_list

    # def get_total_amount(self, obj):
    #     total = 0
    #     prescriptions = MedPrescribed.objects.filter(pharmacist=obj)
    #     for prescription in prescriptions:
    #         for medicine in prescription.med_list.all():
    #             total += medicine.unit_price * (prescription.morning + prescription.noon + prescription.night)
    #     return total



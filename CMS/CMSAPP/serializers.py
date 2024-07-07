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
    #dept
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    #qualification
    qualification = QualificationSerializer(read_only = True)
    qualification_id = serializers.PrimaryKeyRelatedField(queryset=Qualification.objects.all())
    #specilization
    specialization = SpecializationSerializer(read_only=True)
    specialization_id = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all())
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
        department = validated_data.pop('department_id')
        qualification = validated_data.pop('qualification_id')
        specialization = validated_data.pop('specialization_id')
        gender = validated_data.pop('gender_id')
        role = validated_data.pop('role_id')
        #for hasing the password
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        user = User.objects.create(
            **validated_data
        )
        user.department = department
        user.qualification = qualification
        user.specialization = specialization
        user.gender = gender
        user.role = role

        user.save()
        
        return user
    
    def update(self,instance,validated_data):
        department_data = validated_data.pop('department_id')
        qualification_data = validated_data.pop('qualification_id')
        specialization_data = validated_data.pop('specialization_id')
        gender_data = validated_data.pop('gender_id')
        role_data = validated_data.pop('role_id')
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



#stock_management serializers
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    suppliee=SupplierSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id','item_name','category','ordered_quantity','supplier','price','order_date','expected_delivery_date','status','suppliee')
    def create(self, validated_data):
        supplier = validated_data.pop('supplier', None)
        order = (Order.objects.create(**validated_data,supplier=supplier))
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['suppliee'] = SupplierSerializer(instance.supplier).data

        return rep
    


    
class EquipmentSerializer(serializers.ModelSerializer):
    suppliee=SupplierSerializer(read_only=True)
    class Meta:
        model = Equipment
        fields = ('id','name','description','supplier','quantity','reorder_level','purchase_date','warranty_expiry','suppliee')
    def create(self, validated_data):
        supplier = validated_data.pop('supplier', None)
        order = (Equipment.objects.create(**validated_data,supplier=supplier))
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['suppliee'] = SupplierSerializer(instance.supplier).data

        return rep
class MiscellaneousItemSerializer(serializers.ModelSerializer):
    suppliee=SupplierSerializer(read_only=True)
    class Meta:
        model = MiscellaneousItem
        fields = ('id','name','description','supplier','quantity','reorder_level','suppliee')
    def create(self, validated_data):
        supplier = validated_data.pop('supplier', None)
        order = (MiscellaneousItem.objects.create(**validated_data,supplier=supplier))
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['suppliee'] = SupplierSerializer(instance.supplier).data

        return rep
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
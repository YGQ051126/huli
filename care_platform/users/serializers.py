from rest_framework import serializers
from typing import TYPE_CHECKING
from .models import User, FamilyUser, StaffUser, LeaveRequest
from patients.models import Patient

if TYPE_CHECKING:
    from django.db.models import QuerySet

class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    staff_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'phone', 'email', 'role', 'status', 'gender', 'avatar', 'created_at', 'updated_at', 'staff_info']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_staff_info(self, obj):
        if obj.role == 'staff' and hasattr(obj, 'staffuser'):
            return {
                'id': obj.staffuser.pk,  # type: ignore
                'position': obj.staffuser.position,  # type: ignore
                'department': obj.staffuser.department  # type: ignore
            }
        return None

class UserCreateSerializer(serializers.ModelSerializer):
    """????????"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'real_name', 'phone', 'email', 'role', 'status', 'gender', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'status': {'required': False, 'default': 'active'},
        }
    
    def create(self, validated_data):
        # Plain text password storage as requested
        user = User.objects.create(  # type: ignore[attr-defined]
            username=validated_data['username'],
            password=validated_data['password'],
            real_name=validated_data['real_name'],
            phone=validated_data['phone'],
            email=validated_data.get('email'),
            role=validated_data['role'],
            status=validated_data.get('status', 'active'),
            gender=validated_data.get('gender'),
            avatar=validated_data.get('avatar'),
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class FamilyUserSerializer(serializers.ModelSerializer):
    """Family user serializer"""
    user = UserSerializer(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())  # type: ignore[attr-defined]
    
    class Meta:
        model = FamilyUser
        fields = ['user', 'patient', 'relationship', 'proof_file', 'status', 'balance', 'created_at', 'updated_at']

class FamilyUserCreateSerializer(serializers.ModelSerializer):
    
    user = UserCreateSerializer()
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())  # type: ignore[attr-defined]
    
    class Meta:
        model = FamilyUser
        fields = ['user', 'patient', 'relationship', 'proof_file']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        # Plain text password storage as requested
        user = User.objects.create(  # type: ignore[attr-defined]
            username=user_data['username'],
            password=user_data['password'],
            real_name=user_data['real_name'],
            phone=user_data['phone'],
            email=user_data.get('email'),
            role='family',
            status='pending',
            gender=user_data.get('gender'),
            avatar=user_data.get('avatar'),
        )
        family_user = FamilyUser.objects.create(  # type: ignore[attr-defined]
            user=user,
            patient=validated_data['patient'],
            relationship=validated_data['relationship'],
            proof_file=validated_data.get('proof_file'),
        )
        return family_user

class StaffUserSerializer(serializers.ModelSerializer):
    """Staff user serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StaffUser
        fields = ['user', 'position', 'department', 'created_at', 'updated_at']

class StaffUserCreateSerializer(serializers.ModelSerializer):
    """Staff user create serializer"""
    user = UserCreateSerializer()
    
    class Meta:
        model = StaffUser
        fields = ['user', 'position', 'department']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(  # type: ignore[attr-defined]
            username=user_data['username'],
            password=user_data['password'],
            real_name=user_data['real_name'],
            phone=user_data['phone'],
            email=user_data.get('email'),
            role='staff',
            status='active',
            gender=user_data.get('gender'),
            avatar=user_data.get('avatar'),
        )
        staff_user = StaffUser.objects.create(  # type: ignore[attr-defined]
            user=user,
            position=validated_data['position'],
            department=validated_data['department'],
        )
        return staff_user

class AuthResponseSerializer(serializers.Serializer):
    """Auth response serializer"""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField(required=False)
    user = UserSerializer()
    profile = serializers.SerializerMethodField()
    
    def get_profile(self, obj):
        user = obj['user']
        if user.role == 'family':
            try:
                family_user = FamilyUser.objects.get(user=user)  # type: ignore[attr-defined]
                return FamilyUserSerializer(family_user).data
            except FamilyUser.DoesNotExist:  # type: ignore[attr-defined]
                return {}
        elif user.role == 'staff':
            try:
                staff_user = StaffUser.objects.get(user=user)  # type: ignore[attr-defined]
                return StaffUserSerializer(staff_user).data
            except StaffUser.DoesNotExist:  # type: ignore[attr-defined]
                return {}
        return {}

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    class Meta:
        model = User
        fields = ['id', 'real_name', 'phone', 'email', 'avatar', 'role']
        read_only_fields = ['id', 'role']

class StaffUserUpdateSerializer(serializers.ModelSerializer):
    """Staff user update serializer"""
    
    class Meta:
        model = StaffUser
        fields = ['position', 'department']
        
    def update(self, instance, validated_data):
        # ĂĹĽÂ¸ĂźÄĂ StaffUser ÄžĂ position ĹĂ department ĂĂĹĂ
        instance.position = validated_data.get('position', instance.position)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        return instance

from .models import User, FamilyUser, StaffUser, LeaveRequest, RegisterApplication

class RegisterApplicationSerializer(serializers.ModelSerializer):
    """Registration Application Serializer"""
    
    class Meta:
        model = RegisterApplication
        fields = '__all__'
        read_only_fields = ['status', 'approved_by', 'approved_at', 'rejection_reason', 'created_at', 'updated_at']
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("ÓĂť§ĂűŇŃ´ćÔÚ")
        if RegisterApplication.objects.filter(username=value, status='pending').exists():
            raise serializers.ValidationError("¸ĂÓĂť§ĂűŇŃÔÚÉęÇëÖĐ")
        return value

class LeaveRequestSerializer(serializers.ModelSerializer):
    """Leave request serializer"""
    staff_name = serializers.CharField(source='staff.user.real_name', read_only=True)
    department = serializers.CharField(source='staff.department', read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['staff', 'status', 'approved_by', 'approved_at', 'created_at', 'updated_at']

from rest_framework import serializers
from .models import Appointment, AppointmentTimeSlot
from users.serializers import UserSerializer, FamilyUserSerializer, StaffUserSerializer
from patients.serializers import PatientSerializer
from users.models import FamilyUser
from patients.models import Patient

class AppointmentTimeSlotSerializer(serializers.ModelSerializer):
    """预约时间段序列化器"""
    class Meta:
        model = AppointmentTimeSlot
        fields = ['id', 'start_time', 'end_time', 'is_available', 'max_appointments']
        read_only_fields = ['id']

class AppointmentSerializer(serializers.ModelSerializer):
    """预约序列化器"""
    patient = PatientSerializer(read_only=True)
    family_user = FamilyUserSerializer(read_only=True)
    staff_user = StaffUserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    
    # Flattened fields for easy frontend access
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    family_name = serializers.CharField(source='family_user.user.real_name', read_only=True)
    reviewer_name = serializers.CharField(source='approved_by.real_name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'type', 'patient', 'family_user', 'staff_user', 'date', 'time_slot', 'status', 'notes', 'approved_by', 'approved_at', 'created_at', 'updated_at', 'patient_name', 'family_name', 'reviewer_name']
        read_only_fields = ['id', 'approved_by', 'approved_at', 'created_at', 'updated_at']

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """预约创建序列化器"""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    family_user = serializers.PrimaryKeyRelatedField(queryset=FamilyUser.objects.all(), required=False)
    
    class Meta:
        model = Appointment
        fields = ['type', 'patient', 'family_user', 'date', 'time_slot', 'notes']

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """预约更新序列化器"""
    class Meta:
        model = Appointment
        fields = ['status', 'notes', 'staff_user']

class AppointmentApproveSerializer(serializers.ModelSerializer):
    """预约审批序列化器"""
    class Meta:
        model = Appointment
        fields = ['status', 'notes']
        extra_kwargs = {
            'status': {'required': True},
        }
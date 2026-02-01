from rest_framework import serializers
from .models import (
    Service, CustomServiceRequest, ServiceExecution,
    ServiceOrder, ServiceOrderItem, ServiceFeedback,
    ServiceFeedbackImage, ServiceReview
)
from users.serializers import FamilyUserSerializer, StaffUserSerializer, UserSerializer
from patients.serializers import PatientSerializer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class CustomServiceRequestSerializer(serializers.ModelSerializer):
    family = FamilyUserSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomServiceRequest
        fields = '__all__'
        extra_kwargs = {
            'family': {'required': False},
            'approved_by': {'required': False},
            'approved_at': {'required': False},
        }

class ServiceExecutionSerializer(serializers.ModelSerializer):
    custom_service = CustomServiceRequestSerializer(read_only=True)
    staff = StaffUserSerializer(read_only=True)
    
    class Meta:
        model = ServiceExecution
        fields = '__all__'
        extra_kwargs = {
            'custom_service': {'required': False},
            'staff': {'required': False},
        }

# --- New Serializers ---

class ServiceOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrderItem
        fields = ['id', 'service', 'service_name', 'price']

class ServiceFeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeedbackImage
        fields = ['id', 'image', 'created_at']

class ServiceFeedbackSerializer(serializers.ModelSerializer):
    images = ServiceFeedbackImageSerializer(many=True, read_only=True)
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)

    class Meta:
        model = ServiceFeedback
        fields = ['id', 'staff', 'staff_name', 'content', 'images', 'created_at']

class ServiceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = ['id', 'rating', 'comment', 'created_at']

class ServiceOrderSerializer(serializers.ModelSerializer):
    items = ServiceOrderItemSerializer(many=True, read_only=True)
    feedback = ServiceFeedbackSerializer(read_only=True)
    review = ServiceReviewSerializer(read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    family_name = serializers.CharField(source='family.user.get_full_name', read_only=True)

    class Meta:
        model = ServiceOrder
        fields = [
            'id', 'order_no', 'family', 'family_name', 'patient', 'patient_name',
            'total_amount', 'status', 'paid_at', 'created_at',
            'items', 'feedback', 'review'
        ]
        read_only_fields = ['order_no', 'family', 'total_amount', 'status', 'paid_at', 'created_at']

class CreateServiceOrderSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

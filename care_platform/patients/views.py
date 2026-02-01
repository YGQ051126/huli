from rest_framework import viewsets, generics
from rest_framework.views import APIView
from typing import TYPE_CHECKING
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from payments.models import Bill
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from utils.permissions import IsAdminUser, IsStaffUser, IsFamilyUser, IsFamilyOfPatient
from utils.response import APIResponse, ErrorResponse, success_response, error_response
from .models import Patient, HealthAssessment, MedicalRecord
from rooms.models import Room
from .serializers import (
    PatientSerializer,
    PatientCreateSerializer,
    PatientDetailSerializer,
    HealthAssessmentSerializer,
    HealthAssessmentCreateSerializer,
    MedicalRecordSerializer,
    MedicalRecordCreateSerializer
)

try:
    if TYPE_CHECKING:
        from django.db.models import QuerySet
except ImportError:
    pass

class PatientViewSet(viewsets.ModelViewSet):
    """Patient ViewSet"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get_permissions(self):
        """Get permissions based on action"""
        # Allow all users to access all actions
        return []
    
    def get_serializer_class(self):
        """Get serializer class based on action"""
        if self.action == 'create':
            return PatientCreateSerializer
        elif self.action == 'retrieve':
            return PatientDetailSerializer
        return PatientSerializer
    
    def list(self, request, *args, **kwargs):
        """Get patient list with custom response format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create patient and return complete data"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get room and bed info
        room_number = serializer.validated_data.get('room')
        bed_id = serializer.validated_data.get('bed_id')
        patient_name = serializer.validated_data.get('name')
        
        # Update Room table logic
        if room_number and bed_id:
            try:
                # 1. Query Room
                room_obj = Room.objects.filter(room_number=room_number).first()
                if not room_obj:
                    return error_response(code=400, message=f'房间�? {room_number} 不存�?')
                
                # 2. Determine bed field
                # bed_id might be "1" or "4"
                bed_suffix = str(bed_id).strip()
                if bed_suffix not in ['1', '2', '3', '4']:
                     return error_response(code=400, message=f'床位�? {bed_id} 无效，必须是 1-4')
                
                bed_field_name = f'bed{bed_suffix}'
                
                # 3. Check if occupied
                current_occupant = getattr(room_obj, bed_field_name)
                if current_occupant:
                    return error_response(code=400, message=f'房间 {room_number} �? {bed_id} 号床位已�? {current_occupant} 占用')
                
                # 4. Update Room
                setattr(room_obj, bed_field_name, patient_name)
                room_obj.save()
                print(f"Updated room {room_number} {bed_field_name} to {patient_name}")
                
            except Exception as e:
                # Manual rollback if needed, but atomic should handle database errors
                print(f"Error updating room bed: {e}")
                raise e
                
        self.perform_create(serializer)
        # Use PatientSerializer to return complete data
        response_serializer = PatientSerializer(serializer.instance)
        return success_response(response_serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Update patient and return complete data"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        
        if not serializer.is_valid():
            return error_response(code=400, message=f'Validation failed: {serializer.errors}')
        
        # Get new room and bed info
        new_room_number = serializer.validated_data.get('room')
        new_bed_id = serializer.validated_data.get('bed_id')
        new_patient_name = serializer.validated_data.get('name')
        
        # Check if room/bed changed
        old_room_number = instance.room
        old_bed_id = instance.bed_id
        
        # If room or bed info exists and changed
        if new_room_number and new_bed_id:
            # Check if logically changed
            if new_room_number != old_room_number or str(new_bed_id) != str(old_bed_id):
                try:
                    # 1. Query New Room
                    new_room_obj = Room.objects.filter(room_number=new_room_number).first()
                    if not new_room_obj:
                        return error_response(code=400, message=f'房间�? {new_room_number} 不存�?')
                    
                    # 2. Determine bed field
                    bed_suffix = str(new_bed_id).strip()
                    if bed_suffix not in ['1', '2', '3', '4']:
                         return error_response(code=400, message=f'床位�? {new_bed_id} 无效，必须是 1-4')
                    
                    bed_field_name = f'bed{bed_suffix}'
                    
                    # 3. Check if occupied (allow if it's the same person, though unlikely in this logic path if keys changed)
                    current_occupant = getattr(new_room_obj, bed_field_name)
                    if current_occupant and current_occupant != instance.name: # Assuming name didn't change, or even if it did, check if it's not empty
                         return error_response(code=400, message=f'房间 {new_room_number} �? {new_bed_id} 号床位已�? {current_occupant} 占用')
                    
                    # 4. Update New Room
                    setattr(new_room_obj, bed_field_name, new_patient_name)
                    new_room_obj.save()
                    
                    # 5. Clear Old Room Bed (Optional but recommended for consistency)
                    if old_room_number and old_bed_id:
                        old_room_obj = Room.objects.filter(room_number=old_room_number).first()
                        if old_room_obj:
                            old_bed_suffix = str(old_bed_id).strip()
                            old_bed_field = f'bed{old_bed_suffix}'
                            if hasattr(old_room_obj, old_bed_field):
                                # Only clear if it was this patient
                                if getattr(old_room_obj, old_bed_field) == instance.name:
                                    setattr(old_room_obj, old_bed_field, None) # Or empty string? Model says blank=True, null=True.
                                    old_room_obj.save()

                except Exception as e:
                    print(f"Error updating room bed: {e}")
                    raise e
        
        # If just name changed, update room record?
        elif (not new_room_number and not new_bed_id) and (old_room_number and old_bed_id):
             # Maybe clearing? The requirement doesn't specify clearing logic, focused on assignment.
             pass

        self.perform_update(serializer)
        
        # Use PatientSerializer to return complete data
        response_serializer = PatientSerializer(serializer.instance)
        return success_response(response_serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get patient detail including latest health assessment"""
        instance = self.get_object()
        latest_health_assessment = instance.healthassessment_set.order_by('-assessment_date').first()
        
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        
        if latest_health_assessment:
            health_serializer = HealthAssessmentSerializer(latest_health_assessment)
            response_data['latest_health_assessment'] = health_serializer.data
        else:
            response_data['latest_health_assessment'] = None
        
        return success_response(response_data)

class HealthAssessmentViewSet(viewsets.ModelViewSet):
    """Health Assessment ViewSet"""
    queryset = HealthAssessment.objects.all()
    serializer_class = HealthAssessmentSerializer
    
    def get_permissions(self):
        """Get permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        else:
            return [IsStaffUser()]
    
    def get_serializer_class(self):
        """Get serializer class based on action"""
        if self.action == 'create':
            return HealthAssessmentCreateSerializer
        return HealthAssessmentSerializer
    
    def perform_create(self, serializer):
        """Save health assessment, automatically associate creator"""
        serializer.save(created_by=self.request.user)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    """Medical Record ViewSet"""
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    
    def get_permissions(self):
        """Get permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        else:
            return [IsStaffUser()]
    
    def get_serializer_class(self):
        """Get serializer class based on action"""
        if self.action == 'create':
            return MedicalRecordCreateSerializer
        return MedicalRecordSerializer
    
    def perform_create(self, serializer):
        """Save medical record, automatically associate doctor"""
        serializer.save(doctor=self.request.user)

class PatientHealthAssessmentsView(generics.ListAPIView):
    """Get patient's health assessment list"""
    serializer_class = HealthAssessmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return HealthAssessment.objects.filter(patient_id=patient_id).order_by('-assessment_date')  # type: ignore

class PatientMedicalRecordsView(generics.ListAPIView):
    """Get patient's medical record list"""
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return MedicalRecord.objects.filter(patient_id=patient_id).order_by('-record_date')  # type: ignore

class FamilyPatientListView(generics.ListAPIView):
    """Family user get associated patient list"""
    serializer_class = PatientSerializer
    permission_classes = [IsFamilyUser]
    
    def get_queryset(self):
        """Get current family user's associated patient list"""
        family_user = getattr(self.request.user, 'familyuser', None) # type: ignore
        if not family_user:
             return []
        return [family_user.patient]

class FamilyPatientDetailView(generics.RetrieveAPIView):
    """Family user get single patient detail"""
    serializer_class = PatientDetailSerializer
    permission_classes = [IsFamilyUser, IsFamilyOfPatient]
    
    def get_queryset(self):
        """Get current family user's associated patient"""
        family_user = getattr(self.request.user, 'familyuser', None)  # type: ignore
        if not family_user or not family_user.patient:
            return Patient.objects.none()  # type: ignore
        return Patient.objects.filter(id=family_user.patient.id)  # type: ignore

class FamilyDashboardView(APIView):
    permission_classes = [IsFamilyUser]
    
    def get(self, request):
        try:
            family_user = getattr(request.user, 'familyuser', None) # type: ignore
            if not family_user:
                 return error_response(message="Not a family user")
                 
            patient = family_user.patient
            
            if not patient:
                return success_response({})
            
            # 1. 院民基本信息
            patient_serializer = PatientSerializer(patient)
            patient_data = patient_serializer.data
            
            # �ֶ�ע�뷿������
            if patient.room:
                try:
                    room_obj = Room.objects.filter(room_number=patient.room).first()
                    if room_obj:
                        patient_data['room'] = {
                            'room_number': room_obj.room_number,
                            'id': room_obj.id,
                            # ��������������Ҫ���ֶ�
                        }
                except Exception as e:
                    print(f"Error fetching room details: {e}")
            
            # 2. 最新通知 (取最�3�)
            recent_notifications = Notification.objects.filter(  # type: ignore
                user=request.user
            ).order_by('-created_at')[:3]
            notifications_data = NotificationSerializer(recent_notifications, many=True).data
            
            # 3. 待缴费账单数
            unpaid_bills_count = Bill.objects.filter(  # type: ignore
                patient=patient, 
                status__in=['unpaid', 'partially_paid']
            ).count()
            
            return success_response({
                'patient': patient_data,
                'recent_notifications': notifications_data,
                'unpaid_bills_count': unpaid_bills_count,
            })
        except Exception as e:
            # 如果�? FamilyUser.DoesNotExist 等错�?
            return error_response(message=str(e))

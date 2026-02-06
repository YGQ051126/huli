# -*- coding: utf-8 -*-
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from utils.permissions import IsStaffUser, IsAdminUser, IsFamilyUser, IsFamilyOfPatient
from utils.response import success_response, error_response
from .models import CareRecord, CareTemplate, VitalSigns, DailyCareTask
from patients.models import Patient
from .serializers import (
    CareRecordSerializer,
    CareRecordCreateSerializer,
    CareRecordUpdateSerializer,
    CareTemplateSerializer,
    CareTemplateCreateSerializer,
    CareTemplateUpdateSerializer,
    VitalSignsSerializer,
    DailyCareTaskSerializer
)

class CareRecordViewSet(viewsets.ModelViewSet):
    """Care Record ViewSet"""
    queryset = CareRecord.objects.all()
    serializer_class = CareRecordSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'submit']:
            return [IsStaffUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CareRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CareRecordUpdateSerializer
        return CareRecordSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        care_record = serializer.save()
        
        return success_response(
            CareRecordSerializer(care_record).data,
            code=201,
            message='Care record saved successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        care_record = serializer.save()
        
        return success_response(
            CareRecordSerializer(care_record).data,
            message='Care record updated successfully'
        )

    @action(detail=False, methods=['post'])
    def submit(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        care_record = serializer.save()
        
        return success_response(
            CareRecordSerializer(care_record).data,
            code=201,
            message='Care record submitted successfully'
        )

class CareTemplateByPatientView(generics.RetrieveAPIView):
    """Get care template by patient"""
    serializer_class = CareTemplateSerializer
    permission_classes = [IsStaffUser]

    def get_object(self):
        # Using request.GET or query_params (DRF)
        query_params = getattr(self.request, 'query_params', self.request.GET)
        patient_id = query_params.get('patient_id')
        if not patient_id:
            return None
        
        try:
            patient = Patient.objects.get(pk=patient_id)
            template = CareTemplate.objects.filter(
                care_level=patient.care_level, 
                is_active=True
            ).first()
            
            if not template:
                template = CareTemplate.objects.filter(is_active=True).first()
            
            # If still no template, create a default in-memory one or db one
            if not template:
                # Create a default template with standard fields
                default_fields = [
                    {
                        "id": "diet",
                        "label": "Diet",
                        "type": "select",
                        "options": [
                            {"label": "Normal", "value": "normal"},
                            {"label": "Poor Appetite", "value": "poor"},
                            {"label": "Refused", "value": "refused"},
                            {"label": "Semi-liquid", "value": "semi_liquid"},
                            {"label": "Liquid", "value": "liquid"}
                        ]
                    },
                    {
                        "id": "bowel",
                        "label": "Bowel Movement",
                        "type": "select",
                        "options": [
                            {"label": "Normal", "value": "normal"},
                            {"label": "Constipation", "value": "constipation"},
                            {"label": "Diarrhea", "value": "diarrhea"},
                            {"label": "Incontinence", "value": "incontinence"}
                        ]
                    },
                    {
                        "id": "mental",
                        "label": "Mental Status",
                        "type": "select",
                        "options": [
                            {"label": "Clear", "value": "clear"},
                            {"label": "Sleepy", "value": "sleepy"},
                            {"label": "Agitated", "value": "agitated"},
                            {"label": "Coma", "value": "coma"}
                        ]
                    },
                    {
                        "id": "sleep",
                        "label": "Sleep",
                        "type": "select",
                        "options": [
                            {"label": "Good", "value": "good"},
                            {"label": "Fair", "value": "fair"},
                            {"label": "Poor", "value": "poor"}
                        ]
                    },
                    {
                        "id": "hygiene",
                        "label": "Personal Hygiene",
                        "type": "checkbox_group",
                        "options": [
                            {"label": "Bath", "value": "bath"},
                            {"label": "Hair Wash", "value": "hair_wash"},
                            {"label": "Nail Cut", "value": "nail_cut"},
                            {"label": "Oral Care", "value": "oral_care"}
                        ]
                    },
                    {
                        "id": "notes",
                        "label": "Notes",
                        "type": "textarea",
                        "placeholder": "Enter other abnormalities or notes"
                    }
                ]
                
                # Check if we should save it or just return transient
                # Let's save it as a "Default Template"
                template = CareTemplate.objects.create(
                    name="Standard Care Template",
                    care_level="all",
                    template_content={"fields": default_fields},
                    is_active=True
                )
                
            return template
        except Patient.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return error_response(code=404, message="No suitable care template found")
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data)


class PatientCareRecordsView(generics.ListAPIView):
    serializer_class = CareRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return CareRecord.objects.filter(patient_id=patient_id).order_by('-record_date', '-record_time')

class StaffCareRecordsView(generics.ListAPIView):
    serializer_class = CareRecordSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        staff_id = self.kwargs['staff_id']
        return CareRecord.objects.filter(staff_id=staff_id).order_by('-record_date', '-record_time')

class FamilyCareRecordsView(generics.ListAPIView):
    serializer_class = CareRecordSerializer
    permission_classes = [IsFamilyUser]
    
    def get_queryset(self):
        if not hasattr(self.request.user, 'familyuser'):
            return CareRecord.objects.none()
        family_user = getattr(self.request.user, 'familyuser', None)
        if not family_user:
             return CareRecord.objects.none()
        return CareRecord.objects.filter(patient=family_user.patient).order_by('-record_date', '-record_time')

class CareTemplateViewSet(viewsets.ModelViewSet):
    queryset = CareTemplate.objects.all()
    serializer_class = CareTemplateSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsStaffUser()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsStaffUser()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CareTemplateCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CareTemplateUpdateSerializer
        return CareTemplateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        care_template = serializer.save()
        
        return success_response(
            CareTemplateSerializer(care_template).data,
            code=201,
            message='Care template created successfully'
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        care_template = serializer.save()
        
        return success_response(
            CareTemplateSerializer(care_template).data,
            message='Care template updated successfully'
        )

class ActiveCareTemplatesView(generics.ListAPIView):
    serializer_class = CareTemplateSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        return CareTemplate.objects.filter(is_active=True)

class CareTemplateByLevelView(generics.ListAPIView):
    serializer_class = CareTemplateSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        care_level = self.kwargs['care_level']
        return CareTemplate.objects.filter(care_level=care_level, is_active=True)

class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer
    permission_classes = [IsStaffUser]
    
    def get_serializer_class(self):
        return VitalSignsSerializer

class DailyCareTaskViewSet(viewsets.ModelViewSet):
    queryset = DailyCareTask.objects.all()
    serializer_class = DailyCareTaskSerializer
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        queryset = DailyCareTask.objects.all()
        
        # Filter by patient if provided
        # Use query_params for DRF Request, or GET for standard Django Request
        query_params = getattr(self.request, 'query_params', self.request.GET)
        patient_id = query_params.get('patient')
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        else:
            # Default to today's tasks ONLY if no patient filter is present
            # This maintains backward compatibility for the dashboard view
            today = timezone.now().date()
            queryset = queryset.filter(task_date=today)
            
        return queryset

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        tasks = DailyCareTask.objects.filter(task_date=today)
        
        # Lazy generation: if no tasks exist for today, generate them for all patients
        if not tasks.exists():
            from patients.models import Patient
            patients = Patient.objects.all() # Fetch all patients
            
            new_tasks = []
            for patient in patients:
                new_tasks.append(DailyCareTask(
                    patient=patient,
                    task_date=today
                ))
            if new_tasks:
                DailyCareTask.objects.bulk_create(new_tasks)
                tasks = DailyCareTask.objects.filter(task_date=today)
            
        serializer = self.get_serializer(tasks, many=True)
        return success_response(serializer.data)

    @action(detail=False, methods=['post'])
    def batch_update(self, request):
        data = request.data.get('tasks', [])
        if not data:
            return error_response(message="No tasks provided")
        
        try:
            with transaction.atomic():
                updated_tasks = []
                for item in data:
                    task_id = item.get('id')
                    if not task_id:
                        continue
                    
                    try:
                        task = DailyCareTask.objects.get(id=task_id)
                        # Only update fields if provided
                        if 'vital_signs_normal' in item:
                            task.vital_signs_normal = item['vital_signs_normal']
                        if 'diet_normal' in item:
                            task.diet_normal = item['diet_normal']
                        if 'mental_normal' in item:
                            task.mental_normal = item['mental_normal']
                        if 'is_completed' in item:
                            task.is_completed = item['is_completed']
                        
                        if hasattr(request.user, 'staffuser'):
                            task.last_updated_by = request.user.staffuser
                            
                        task.save()
                        updated_tasks.append(task)
                    except DailyCareTask.DoesNotExist:
                        continue
                
                return success_response(
                    DailyCareTaskSerializer(updated_tasks, many=True).data,
                    message="Tasks updated successfully"
                )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return error_response(message=str(e), code=500)

    @action(detail=False, methods=['get'])
    def pull_latest(self, request):
        return self.today(request)

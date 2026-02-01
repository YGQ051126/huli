from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from utils.permissions import IsAdminUser, IsStaffUser, IsFamilyUser, IsFamilyOfPatient, IsStaffOrAdmin
from utils.response import APIResponse, ErrorResponse, success_response, error_response
from .models import Appointment, AppointmentTimeSlot
from .serializers import (
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer,
    AppointmentApproveSerializer,
    AppointmentTimeSlotSerializer
)

from rest_framework.decorators import action

from django.db import IntegrityError

class AppointmentViewSet(viewsets.ModelViewSet):
    """Appointment ViewSet"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        """Get appointments based on user role"""
        user = self.request.user
        if not user.is_authenticated:
            return Appointment.objects.none()
            
        role = getattr(user, 'role', None)
        if role == 'family':
            # Safely check for familyuser
            if hasattr(user, 'familyuser'):
                return Appointment.objects.filter(family_user=user.familyuser) # type: ignore
            return Appointment.objects.none()
            
        return Appointment.objects.all()
    
    def get_permissions(self):
        """Get permissions based on action"""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['list', 'retrieve', 'cancel']:
            return [IsAuthenticated()]
        else:
            return [IsStaffOrAdmin()]
    
    def get_serializer_class(self):
        """Get serializer based on action"""
        if self.action == 'create':
            return AppointmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer
    
    def create(self, request, *args, **kwargs):
        """Create appointment"""
        data = request.data.copy()
        
        # Auto-fill family_user and patient for family users
        role = getattr(request.user, 'role', None)
        if role == 'family':
             # Safely check for familyuser
             if not hasattr(request.user, 'familyuser'):
                 return error_response(code=400, message='User profile incomplete. Please contact administrator.')
             
             family_user = request.user.familyuser # type: ignore
             # FamilyUser's primary key is 'user', which is a OneToOneField to User.
             # So family_user.pk or family_user.user_id should be used.
             # However, FamilyUser model definition: user = models.OneToOneField(User, ..., primary_key=True)
             # So family_user.pk is the user_id.
             data['family_user'] = family_user.pk
             
             # If patient is not provided in data, try to get it from family_user
             if 'patient' not in data or not data['patient'] or data['patient'] == 0:
                if family_user.patient:
                    data['patient'] = family_user.patient.id
                else:
                    return error_response(code=400, message='You are not linked to any patient yet.')
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # Manually create the object to handle potential database errors gracefully
        try:
            appointment = serializer.save()
        except IntegrityError as e:
            print(f"IntegrityError in create appointment: {e}")
            return error_response(code=400, message='Database integrity error. Please check your data.')
        except Exception as e:
            print(f"Error in create appointment: {e}")
            # Check if it's a foreign key error or other known issues
            err_str = str(e)
            if 'patient' in err_str or 'Constraint' in err_str:
                 return error_response(code=400, message='Invalid patient ID or you are not linked to any patient.')
            if 'family_user' in err_str:
                 return error_response(code=400, message='Family user profile missing.')
            # Return generic error for other cases but log it
            return error_response(code=500, message=f'Internal server error: {err_str}')
        
        return success_response(
            AppointmentSerializer(appointment).data,
            code=201,
            message='Appointment request submitted, waiting for approval'
        )

    @action(detail=True, methods=['post'], permission_classes=[IsStaffOrAdmin])
    def approve(self, request, pk=None):
        """Approve appointment"""
        appointment = self.get_object()
        if appointment.status != 'pending':
            return error_response(code=400, message='Appointment is not pending')
            
        appointment.status = 'approved'
        appointment.approved_by = request.user
        appointment.approved_at = timezone.now()
        appointment.save()
        
        return success_response(
            AppointmentSerializer(appointment).data,
            message='Appointment approved'
        )

    @action(detail=True, methods=['post'], permission_classes=[IsStaffOrAdmin])
    def reject(self, request, pk=None):
        """Reject appointment"""
        appointment = self.get_object()
        if appointment.status != 'pending':
            return error_response(code=400, message='Appointment is not pending')
            
        reason = request.data.get('reason', '')
        appointment.status = 'rejected'
        appointment.notes = f"{appointment.notes or ''}\nRefusal Reason: {reason}".strip()
        appointment.approved_by = request.user
        appointment.approved_at = timezone.now()
        appointment.save()
        
        return success_response(
            AppointmentSerializer(appointment).data,
            message='Appointment rejected'
        )

class AppointmentApproveView(generics.GenericAPIView):
    """Appointment Approve View"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentApproveSerializer
    permission_classes = [IsStaffOrAdmin]
    
    def put(self, request, pk):
        """Approve appointment"""
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        appointment = serializer.save(approved_by=request.user)
        appointment.approved_at = timezone.now()
        appointment.save()
        
        return success_response(
            AppointmentSerializer(appointment).data,
            message='Appointment approved'
        )

class AppointmentCancelView(generics.GenericAPIView):
    """Appointment Cancel View"""
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        """Cancel appointment"""
        appointment = self.get_object()
        
        # Check permission: only creator or admin/staff
        if appointment.family_user.user != request.user and request.user.role != 'admin' and request.user.role != 'staff':
            return error_response(code=403, message='No permission to cancel this appointment')
        
        appointment.status = 'cancelled'
        appointment.save()
        
        return success_response(
            AppointmentSerializer(appointment).data,
            message='Appointment cancelled'
        )

class AppointmentTimeSlotViewSet(viewsets.ModelViewSet):
    """Appointment Time Slot ViewSet"""
    queryset = AppointmentTimeSlot.objects.all()
    serializer_class = AppointmentTimeSlotSerializer
    permission_classes = [IsStaffOrAdmin]
    
    def get_serializer_class(self):
        """Get serializer"""
        return AppointmentTimeSlotSerializer

class AvailableTimeSlotsView(generics.ListAPIView):
    """Get available time slots"""
    serializer_class = AppointmentTimeSlotSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get slots for specific date"""
        # Type hint for request to help linter
        request = self.request # type: ignore
        date = request.query_params.get('date') # type: ignore
        queryset = AppointmentTimeSlot.objects.filter(is_available=True)
        if date:
            queryset = queryset.filter(date=date)
        return queryset

class PatientAppointmentsView(generics.ListAPIView):
    """Get appointments for specific patient"""
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Appointment.objects.filter(patient_id=patient_id).order_by('-date', 'time_slot')

class FamilyAppointmentsView(generics.ListAPIView):
    """Get appointments for current family user"""
    serializer_class = AppointmentSerializer
    permission_classes = [IsFamilyUser]
    
    def get_queryset(self):
        family_user = getattr(self.request.user, 'familyuser', None)
        if not family_user:
            return Appointment.objects.none()
        return Appointment.objects.filter(family_user=family_user).order_by('-date', 'time_slot')

class StaffAppointmentsView(generics.ListAPIView):
    """Get appointments for current staff user"""
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        staff_user = getattr(self.request.user, 'staffuser', None)
        if not staff_user:
            return Appointment.objects.none()
        return Appointment.objects.filter(staff_user=staff_user).order_by('-date', 'time_slot')

class PendingAppointmentsView(generics.ListAPIView):
    """Get pending appointments"""
    serializer_class = AppointmentSerializer
    permission_classes = [IsStaffOrAdmin]
    
    def get_queryset(self):
        return Appointment.objects.filter(status='pending').order_by('-created_at')

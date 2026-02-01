from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
import uuid

from .models import (
    Service, CustomServiceRequest, ServiceExecution,
    ServiceOrder, ServiceOrderItem, ServiceFeedback,
    ServiceFeedbackImage, ServiceReview
)
from .serializers import (
    ServiceSerializer, CustomServiceRequestSerializer, ServiceExecutionSerializer,
    ServiceOrderSerializer, CreateServiceOrderSerializer, ServiceFeedbackSerializer
)
from utils.permissions import IsFamilyUser, IsStaffUser, IsAdminUser
from patients.models import Patient

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class CustomServiceViewSet(viewsets.ModelViewSet):
    queryset = CustomServiceRequest.objects.all()
    serializer_class = CustomServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'familyuser'):
            return CustomServiceRequest.objects.filter(family=user.familyuser) # type: ignore
        elif hasattr(user, 'staffuser'):
            return CustomServiceRequest.objects.all()
        elif user.is_superuser:
            return CustomServiceRequest.objects.all()
        return CustomServiceRequest.objects.none()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'familyuser'):
            serializer.save(family=self.request.user.familyuser) # type: ignore

class ServiceApplicationViewSet(viewsets.ModelViewSet):
    queryset = CustomServiceRequest.objects.all()
    serializer_class = CustomServiceRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsFamilyUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class ServiceExecutionViewSet(viewsets.ModelViewSet):
    queryset = ServiceExecution.objects.all()
    serializer_class = ServiceExecutionSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'staffuser'):
            serializer.save(staff=self.request.user.staffuser) # type: ignore

# --- New ViewSets ---

class ServiceOrderViewSet(viewsets.ModelViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'familyuser'):
            return ServiceOrder.objects.filter(family=user.familyuser) # type: ignore
        elif hasattr(user, 'staffuser'):
            # Staff see tasks. For now, seeing all paid tasks or tasks for their patients.
            # Assuming all 'pending' (paid) and 'processing' tasks are visible to staff.
            # Use 'pending' for 'Pending Staff'
            return ServiceOrder.objects.filter(status__in=['pending', 'processing', 'completed', 'rated'])
        elif user.is_superuser:
            return ServiceOrder.objects.all()
        # Fallback for debugging/testing - if user is authenticated but not specifically family/staff/admin, maybe show nothing or check permissions logic
        # For now, let's keep it restrictive
        return ServiceOrder.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[IsFamilyUser])
    def create_order(self, request):
        try:
            serializer = CreateServiceOrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            patient_id = serializer.validated_data['patient_id'] # type: ignore
            service_ids = serializer.validated_data['service_ids'] # type: ignore
            
            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

            services = Service.objects.filter(id__in=service_ids)
            if not services:
                return Response({'error': 'No valid services found'}, status=status.HTTP_400_BAD_REQUEST)

            total_amount = sum(s.price for s in services)
            order_no = f"ORD{uuid.uuid4().hex[:8].upper()}"
            
            # Ensure family profile exists
            if not hasattr(request.user, 'familyuser'):
                 return Response({'error': 'User profile incomplete (FamilyUser missing)'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                order = ServiceOrder.objects.create(
                    order_no=order_no,
                    family=request.user.familyuser, # type: ignore
                    patient=patient,
                    total_amount=total_amount,
                    status='pending', # Paid, waiting for staff
                    paid_at=timezone.now()
                )
                for s in services:
                    ServiceOrderItem.objects.create(
                        order=order,
                        service=s,
                        service_name=s.name,
                        price=s.price
                    )
            
            return Response(ServiceOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[IsStaffUser])
    def process(self, request, pk=None):
        """Staff marks order as 'Processing' (optional step, or implicitly done when submitting feedback)"""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'processing'
            order.save()
            return Response({'status': 'Order processing started'})
        return Response({'error': 'Order cannot be processed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsStaffUser])
    def submit_feedback(self, request, pk=None):
        try:
            order = self.get_object()
            content = request.data.get('content')
            images = request.FILES.getlist('images')
            
            if not content:
                 return Response({'error': 'Feedback content is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check staff profile
            if not hasattr(request.user, 'staffuser'):
                 return Response({'error': 'User profile incomplete (StaffUser missing)'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                feedback, created = ServiceFeedback.objects.get_or_create(
                    order=order,
                    defaults={'staff': request.user.staffuser, 'content': content} # type: ignore
                )
                if not created:
                    feedback.content = content
                    feedback.save()
                
                # Handle images
                for img in images:
                    ServiceFeedbackImage.objects.create(
                        feedback=feedback,
                        image=img
                    )
                
                order.status = 'completed'
                order.save()
                
            return Response({'status': 'Feedback submitted, order completed'})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], permission_classes=[IsFamilyUser])
    def submit_review(self, request, pk=None):
        order = self.get_object()
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        
        if not rating:
            return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        ServiceReview.objects.create(
            order=order,
            rating=rating,
            comment=comment
        )
        order.status = 'rated'
        order.save()
        return Response({'status': 'Review submitted'})

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def stats(self, request):
        try:
            # Statistics: Total Amount by Month
            # Using strftime to avoid timezone issues for simple monthly grouping if needed, 
            # or just rely on Django's TruncMonth which handles it if TZ is set up.
            # If database returns invalid datetime, it might be due to MySQL strict mode or TZ data missing.
            # Let's try a simpler aggregation or handle the error.
            
            stats = ServiceOrder.objects.filter(status__in=['completed', 'rated']) \
                .annotate(month=TruncMonth('paid_at')) \
                .values('month') \
                .annotate(total=Sum('total_amount')) \
                .order_by('month')
            
            return Response(stats)
        except Exception as e:
             # Fallback: simple loop aggregation (less efficient but safer if DB functions fail)
             import traceback
             traceback.print_exc()
             
             orders = ServiceOrder.objects.filter(status__in=['completed', 'rated'])
             data = {}
             for order in orders:
                 if order.paid_at:
                     month_str = order.paid_at.strftime('%Y-%m-01')
                     data[month_str] = data.get(month_str, 0) + float(order.total_amount)
            
             result = [{'month': k, 'total': v} for k, v in data.items()]
             result.sort(key=lambda x: x['month'])
             return Response(result)

from django.utils import timezone
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification, CareReminder, ReminderParticipation
from .serializers import NotificationSerializer, CareReminderSerializer, ReminderParticipationSerializer
from utils.permissions import IsFamilyUser, IsStaffUser, IsAdminUser

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'type']
    ordering_fields = ['created_at', 'status']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.status == 'unread' and self.request.data.get('status') == 'read':
            serializer.save(read_at=timezone.now())
            
    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        if notification.status == 'unread':
            notification.status = 'read'
            notification.read_at = timezone.now()
            notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_all(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(status='unread').update(status='read', read_at=timezone.now())
        return Response({'status': 'all cleared'})

class CareReminderViewSet(viewsets.ModelViewSet):
    queryset = CareReminder.objects.all()
    serializer_class = CareReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'type']
    ordering_fields = ['reminder_date', 'created_at']
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'familyuser'):
            return CareReminder.objects.filter(patient__familyuser=user.familyuser)
        elif hasattr(user, 'staffuser'):
            return CareReminder.objects.all()
        elif user.is_superuser:
            return CareReminder.objects.all()
        return CareReminder.objects.none()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [IsAuthenticated()]

class ReminderParticipationViewSet(viewsets.ModelViewSet):
    queryset = ReminderParticipation.objects.all()
    serializer_class = ReminderParticipationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'familyuser'):
            return ReminderParticipation.objects.filter(family=user.familyuser)
        elif hasattr(user, 'staffuser'):
            return ReminderParticipation.objects.all()
        elif user.is_superuser:
            return ReminderParticipation.objects.all()
        return ReminderParticipation.objects.none()
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsFamilyUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'familyuser'):
            serializer.save(family=self.request.user.familyuser)

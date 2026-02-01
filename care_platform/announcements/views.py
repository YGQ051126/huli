from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsAdminUser
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer
from utils.response import success_response

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()  # type: ignore
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Admin can see all announcements
        if hasattr(user, 'role') and user.role == 'admin':
            return Announcement.objects.all()  # type: ignore
        # Other users can only see published announcements
        return Announcement.objects.filter(status='published')  # type: ignore
        
    def get_serializer_class(self):
        if self.action == 'create':
            return AnnouncementCreateSerializer
        return AnnouncementSerializer
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        instance.delete()
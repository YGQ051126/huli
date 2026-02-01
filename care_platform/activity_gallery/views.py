from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.files.storage import default_storage
from .models import Activity, ActivityMedia, ActivityParticipant
from .serializers import ActivitySerializer, ActivityMediaSerializer, ActivityParticipantSerializer
from utils.permissions import IsStaffUser, IsAdminUser, IsStaffOrAdmin
from utils.response import success_response

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().prefetch_related('activitymedia_set')  # type: ignore[attr-defined]
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        print(f"DEBUG: perform_create called. User: {self.request.user}")
        print(f"DEBUG: request.FILES keys: {self.request.FILES.keys()}")
        print(f"DEBUG: request.data keys: {self.request.data.keys()}")
        
        # Handle both staff users and admin users
        staff_profile = getattr(self.request.user, 'staffuser', None)
        if staff_profile:
            activity = serializer.save(staff=staff_profile)
        else:
            # For admin users or other users, create without staff association
            activity = serializer.save()
            
        # Handle media files
        media_files = self.request.FILES.getlist('media_files')  # type: ignore[attr-defined]
        print(f"DEBUG: media_files count: {len(media_files)}")
        
        if media_files:  # type: ignore[truthy-function]
            for file in media_files:
                # Validate file type
                content_type = file.content_type or ''
                print(f"DEBUG: Processing file: {file.name}, Type: {content_type}")
                
                if not content_type.startswith(('image/', 'video/')):
                    print(f"DEBUG: Skipping invalid file type: {content_type}")
                    continue  # Skip invalid files or raise ValidationError
                
                # Save file using default storage
                try:
                    path = default_storage.save(f'activity_media/{file.name}', file)
                    url = default_storage.url(path)
                    print(f"DEBUG: File saved. Path: {path}, URL: {url}")
                    
                    media_type = 'video' if content_type.startswith('video') else 'image'
                    media = ActivityMedia.objects.create(  # type: ignore[attr-defined]
                        activity=activity,
                        media_type=media_type,
                        file_url=url,
                        file_path=path,
                        image_path=path if media_type == 'image' else '',
                        file_name=file.name,
                        file_size=file.size,
                        uploaded_by=self.request.user if self.request.user.is_authenticated else None
                    )
                    print(f"DEBUG: ActivityMedia created. ID: {media.id}")
                except Exception as e:
                    print(f"DEBUG: Error saving file or creating media: {e}")
        else:
            print("DEBUG: No media_files found in request.FILES")
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return success_response(data=serializer.data, code=201, message='活动创建成功')

class ActivityMediaViewSet(viewsets.ModelViewSet):
    queryset = ActivityMedia.objects.all()  # type: ignore[attr-defined]
    serializer_class = ActivityMediaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        activity_id = self.request.query_params.get('activity')
        if activity_id:
            queryset = queryset.filter(activity_id=activity_id)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class ActivityParticipantViewSet(viewsets.ModelViewSet):
    queryset = ActivityParticipant.objects.all()  # type: ignore[attr-defined]
    serializer_class = ActivityParticipantSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        # Handle both staff users and admin users
        staff_profile = getattr(self.request.user, 'staffuser', None)
        if staff_profile:
            serializer.save(staff=staff_profile)
        else:
            # For admin users or other users, create without staff association
            serializer.save()

from rest_framework import serializers
from .models import Announcement
from users.serializers import UserSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'publish_time', 'created_at', 'updated_at', 'created_by']

class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'target_role', 'expire_time', 'status']
        
    def create(self, validated_data):
        user = self.context['request'].user
        return Announcement.objects.create(created_by=user, **validated_data) # type: ignore
from rest_framework import serializers
from .models import Activity, ActivityMedia, ActivityParticipant
from users.serializers import StaffUserSerializer, UserSerializer
from patients.serializers import PatientSerializer

class ActivityParticipantSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    staff = StaffUserSerializer(read_only=True)
    
    class Meta:
        model = ActivityParticipant
        fields = '__all__'

class ActivityMediaSerializer(serializers.ModelSerializer):
    activity = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_by = UserSerializer(read_only=True)
    patients = PatientSerializer(many=True, read_only=True)
    
    class Meta:
        model = ActivityMedia
        fields = '__all__'
        extra_kwargs = {
            'uploaded_by': {'required': False},
        }

class ActivitySerializer(serializers.ModelSerializer):
    staff = StaffUserSerializer(read_only=True)
    media_files = ActivityMediaSerializer(many=True, read_only=True, source='activitymedia_set')
    participants = ActivityParticipantSerializer(many=True, read_only=True, source='activityparticipant_set')
    media_count = serializers.IntegerField(source='activitymedia_set.count', read_only=True)
    cover_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = '__all__'
        extra_kwargs = {
            'staff': {'required': False},
        }

    def get_cover_image(self, obj):
        first_media = obj.activitymedia_set.filter(media_type='image').first()
        return first_media.file_url if first_media else None

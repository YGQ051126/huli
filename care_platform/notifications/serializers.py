from rest_framework import serializers
from .models import Notification, CareReminder, ReminderParticipation
from users.serializers import UserSerializer, FamilyUserSerializer
from patients.serializers import PatientSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'

class CareReminderSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    
    class Meta:
        model = CareReminder
        fields = '__all__'

class ReminderParticipationSerializer(serializers.ModelSerializer):
    reminder = CareReminderSerializer(read_only=True)
    family = FamilyUserSerializer(read_only=True)
    
    class Meta:
        model = ReminderParticipation
        fields = '__all__'

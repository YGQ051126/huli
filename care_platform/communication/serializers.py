from rest_framework import serializers
from .models import Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.real_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.real_name', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'created_at', 'updated_at', 'read_at']

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'content', 'type', 'file_url', 'duration', 'patient']
        
    def create(self, validated_data):
        user = self.context['request'].user
        return Message.objects.create(sender=user, **validated_data)

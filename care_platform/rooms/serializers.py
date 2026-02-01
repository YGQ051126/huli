from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'bed1', 'bed2', 'bed3', 'bed4', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['available_beds'] = instance.get_available_beds()
        data['bed_count'] = instance.get_bed_count()
        return data
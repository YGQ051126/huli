# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CareRecord, VitalSigns, CareTemplate, DailyCareTask
from patients.serializers import PatientSerializer
from users.serializers import StaffUserSerializer, UserSerializer

class VitalSignsSerializer(serializers.ModelSerializer):
    """Vital Signs Serializer"""
    
    class Meta:
        model = VitalSigns
        fields = ['care_record', 'temperature', 'heart_rate', 'systolic_pressure', 'diastolic_pressure', 'respiratory_rate', 'blood_oxygen']
        read_only_fields = ['care_record']

class CareRecordSerializer(serializers.ModelSerializer):
    """Care Record Serializer"""
    patient = PatientSerializer(read_only=True)
    staff = StaffUserSerializer(read_only=True)
    vital_signs = VitalSignsSerializer(read_only=True)
    
    class Meta:
        model = CareRecord
        fields = ['id', 'patient', 'staff', 'record_date', 'record_time', 'vital_signs', 'diet', 'sleep', 'bowel_movement', 'mental_state', 'medications', 'care_activities', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CareRecordCreateSerializer(serializers.ModelSerializer):
    """Care Record Create Serializer"""
    vital_signs = VitalSignsSerializer(required=False)
    custom_fields = serializers.DictField(write_only=True, required=False) # Renamed to avoid conflict
    
    class Meta:
        model = CareRecord
        fields = ['patient', 'staff', 'record_date', 'vital_signs', 'diet', 'sleep', 'bowel_movement', 'mental_state', 'medications', 'care_activities', 'notes', 'custom_fields']
    
    def create(self, validated_data):
        vital_signs_data = validated_data.pop('vital_signs', None)
        fields_data = validated_data.pop('custom_fields', {})
        
        if not validated_data.get('care_activities') and fields_data:
            validated_data['care_activities'] = fields_data
            
        for key in ['diet', 'sleep', 'bowel_movement', 'medications']:
            if key in fields_data and not validated_data.get(key):
                 validated_data[key] = fields_data[key]

        care_record = CareRecord.objects.create(**validated_data)
        
        if vital_signs_data:
            VitalSigns.objects.create(care_record=care_record, **vital_signs_data)
        
        return care_record

class CareRecordUpdateSerializer(serializers.ModelSerializer):
    """Care Record Update Serializer"""
    vital_signs = VitalSignsSerializer(required=False)
    
    class Meta:
        model = CareRecord
        fields = ['vital_signs', 'diet', 'sleep', 'bowel_movement', 'mental_state', 'medications', 'care_activities', 'notes']
    
    def update(self, instance, validated_data):
        vital_signs_data = validated_data.pop('vital_signs', None)
        
        instance = super().update(instance, validated_data)
        
        if vital_signs_data:
            VitalSigns.objects.update_or_create(care_record=instance, defaults=vital_signs_data)
        
        return instance

class CareTemplateSerializer(serializers.ModelSerializer):
    """Care Template Serializer"""
    created_by = UserSerializer(read_only=True)
    template_fields = serializers.SerializerMethodField()
    
    class Meta:
        model = CareTemplate
        fields = ['id', 'name', 'care_level', 'template_content', 'template_fields', 'is_active', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_template_fields(self, obj):
        content = obj.template_content or {}
        if isinstance(content, list):
            return content
        return content.get('fields', [])

class CareTemplateCreateSerializer(serializers.ModelSerializer):
    """Care Template Create Serializer"""
    
    class Meta:
        model = CareTemplate
        fields = ['name', 'care_level', 'template_content', 'is_active']
    
    def create(self, validated_data):
        return CareTemplate.objects.create(created_by=self.context['request'].user, **validated_data)

class CareTemplateUpdateSerializer(serializers.ModelSerializer):
    """Care Template Update Serializer"""
    
    class Meta:
        model = CareTemplate
        fields = ['name', 'care_level', 'template_content', 'is_active']

class DailyCareTaskSerializer(serializers.ModelSerializer):
    """Daily Care Task Serializer"""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_room = serializers.CharField(source='patient.room', read_only=True)
    patient_care_level = serializers.CharField(source='patient.care_level', read_only=True)
    
    class Meta:
        model = DailyCareTask
        fields = [
            'id', 'patient', 'patient_name', 'patient_room', 'patient_care_level', 
            'task_date', 'vital_signs_normal', 'diet_normal', 'mental_normal', 
            'is_completed', 'last_updated_by', 'updated_at'
        ]
        read_only_fields = ['id', 'task_date', 'last_updated_by', 'updated_at']

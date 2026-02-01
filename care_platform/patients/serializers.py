from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from .models import Patient, HealthAssessment, MedicalRecord


class DateFieldWithBeijingTime(serializers.DateField):
    """自定义日期字段，处理北京时间"""
    
    def to_internal_value(self, data):
        """将前端传入的日期转换为北京时间"""
        if data:
            try:
                date_obj = super().to_internal_value(data)
                return date_obj
            except Exception as e:
                raise serializers.ValidationError(f'日期格式错误: {e}')
        return None
    
    def to_representation(self, value):
        """将数据库中的日期转换为字符串表示"""
        if value:
            return value.strftime('%Y-%m-%d')
        return None


class PatientSerializer(serializers.ModelSerializer):
    """院民序列化器"""
    admission_date = DateFieldWithBeijingTime()
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'gender', 'age', 'id_card', 'phone', 'address', 'health_level', 'care_level', 'room', 'bed_id', 'admission_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientCreateSerializer(serializers.ModelSerializer):
    """院民创建序列化器"""
    admission_date = DateFieldWithBeijingTime()
    
    class Meta:
        model = Patient
        fields = ['name', 'gender', 'age', 'id_card', 'phone', 'address', 'health_level', 'care_level', 'room', 'bed_id', 'admission_date', 'status']


class HealthAssessmentSerializer(serializers.ModelSerializer):
    """健康评估序列化器"""
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = HealthAssessment
        fields = ['id', 'patient', 'assessment_date', 'health_level', 'vital_signs', 'chronic_diseases', 'allergies', 'assessment_summary', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'assessment_date', 'created_by', 'created_at', 'updated_at']


class MedicalRecordSerializer(serializers.ModelSerializer):
    """医疗记录序列化器"""
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'record_date', 'diagnosis', 'treatment', 'medications', 'doctor', 'created_at', 'updated_at']
        read_only_fields = ['id', 'record_date', 'doctor', 'created_at', 'updated_at']


class PatientDetailSerializer(serializers.ModelSerializer):
    """院民详情序列化器"""
    latest_health_assessment = HealthAssessmentSerializer(read_only=True)
    admission_date = DateFieldWithBeijingTime()
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'gender', 'age', 'id_card', 'phone', 'address', 'health_level', 'care_level', 'room', 'bed_id', 'admission_date', 'status', 'latest_health_assessment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class HealthAssessmentCreateSerializer(serializers.ModelSerializer):
    """健康评估创建序列化器"""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all()) # type: ignore
    
    class Meta:
        model = HealthAssessment
        fields = ['patient', 'health_level', 'vital_signs', 'chronic_diseases', 'allergies', 'assessment_summary']


class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    """医疗记录创建序列化器"""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all()) # type: ignore
    
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'diagnosis', 'treatment', 'medications']

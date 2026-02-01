# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from typing import Optional


class Patient(models.Model):
    """院民模型"""
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    STATUS_CHOICES = (
        ('active', '在院'),
        ('discharged', '已出院'),
        ('transferred', '已转院'),
    )
    
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    id_card = models.CharField(max_length=18, verbose_name='身份证号')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    medical_history = models.TextField(blank=True, null=True, verbose_name='病史')
    allergies = models.TextField(blank=True, null=True, verbose_name='过敏史')
    blood_type = models.CharField(max_length=10, blank=True, null=True, verbose_name='血型')
    emergency_contact = models.CharField(max_length=100, blank=True, null=True, verbose_name='紧急联系人')
    emergency_phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='紧急联系电话')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    room = models.CharField(max_length=3, blank=True, null=True, verbose_name='房间号')
    bed_id = models.CharField(max_length=1, blank=True, null=True, verbose_name='床位号')
    health_level = models.CharField(max_length=20, blank=True, null=True, verbose_name='健康等级')
    care_level = models.CharField(max_length=20, blank=True, null=True, verbose_name='护理等级')
    primary_nurse = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients', verbose_name='责任护工', limit_choices_to={'role': 'staff'}, db_constraint=False)
    admission_date = models.DateField(blank=True, null=True, verbose_name='入院日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '院民'
        verbose_name_plural = '院民管理'


class PatientDocument(models.Model):
    """院民档案模型"""
    DOCUMENT_TYPE_CHOICES = (
        ('id_card', '身份证'),
        ('medical_certificate', '体检证明'),
        ('insurance', '保险单'),
        ('other', '其他'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='院民')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, verbose_name='档案类型')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_url = models.URLField(verbose_name='文件URL')
    file_size = models.IntegerField(verbose_name='文件大小（字节）')
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='上传人')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    def get_document_type_name(self) -> str:
        """获取文档类型的中文名称"""
        type_mapping = {
            'id_card': '身份证',
            'medical_certificate': '体检证明',
            'insurance': '保险单',
            'other': '其他'
        }
        doc_type = str(self.document_type)  # 显式转换为字符串
        return type_mapping.get(doc_type, doc_type)
    
    def __str__(self):
        return f'{self.patient.name} - {self.get_document_type_name()}'
    
    class Meta:
        verbose_name = '院民档案'
        verbose_name_plural = '院民档案管理'


class PatientHealthRecord(models.Model):
    """院民健康记录模型"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='院民')
    record_type = models.CharField(max_length=100, verbose_name='记录类型')
    content = models.TextField(verbose_name='记录内容')
    recorded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='记录人')
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    
    def __str__(self):
        recorded_date = self.recorded_at.strftime('%Y-%m-%d') if isinstance(self.recorded_at, datetime) else str(self.recorded_at)
        return f'{self.patient.name} - {self.record_type} - {recorded_date}'
    
    class Meta:
        verbose_name = '院民健康记录'
        verbose_name_plural = '院民健康记录管理'
        ordering = ['-recorded_at']


class HealthAssessment(models.Model):
    """健康评估模型"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='院民')
    assessment_date = models.DateTimeField(auto_now_add=True, verbose_name='评估日期')
    health_level = models.CharField(max_length=20, verbose_name='健康等级')
    vital_signs = models.TextField(blank=True, null=True, verbose_name='生命体征')
    chronic_diseases = models.TextField(blank=True, null=True, verbose_name='慢性疾病')
    allergies = models.TextField(blank=True, null=True, verbose_name='过敏史')
    assessment_summary = models.TextField(blank=True, null=True, verbose_name='评估总结')
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        assessment_date_str = self.assessment_date.strftime('%Y-%m-%d') if isinstance(self.assessment_date, datetime) else str(self.assessment_date)
        return f'{self.patient.name} - {assessment_date_str} - {self.health_level}'
    
    class Meta:
        verbose_name = '健康评估'
        verbose_name_plural = '健康评估管理'
        ordering = ['-assessment_date']


class MedicalRecord(models.Model):
    """医疗记录模型"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='院民')
    record_date = models.DateTimeField(auto_now_add=True, verbose_name='记录日期')
    diagnosis = models.TextField(verbose_name='诊断')
    treatment = models.TextField(blank=True, null=True, verbose_name='治疗方案')
    medications = models.TextField(blank=True, null=True, verbose_name='用药情况')
    doctor = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='医生')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        record_date_str = self.record_date.strftime('%Y-%m-%d') if isinstance(self.record_date, datetime) else str(self.record_date)
        diagnosis_preview = str(self.diagnosis)[:50] if self.diagnosis else ''
        return f'{self.patient.name} - {record_date_str} - {diagnosis_preview}'
    
    class Meta:
        verbose_name = '医疗记录'
        verbose_name_plural = '医疗记录管理'
        ordering = ['-record_date']

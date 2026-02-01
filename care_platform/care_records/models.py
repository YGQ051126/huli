# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class CareRecord(models.Model):
    """Care Record Model"""
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='Patient')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.CASCADE, verbose_name='Staff', null=True, blank=True)
    record_date = models.DateField(verbose_name='Record Date')
    record_time = models.TimeField(auto_now_add=True, verbose_name='Record Time')
    vital_signs = models.JSONField(verbose_name='Vital Signs', blank=True, null=True)
    diet = models.JSONField(verbose_name='Diet', blank=True, null=True)
    sleep = models.JSONField(verbose_name='Sleep', blank=True, null=True)
    bowel_movement = models.JSONField(verbose_name='Bowel Movement', blank=True, null=True)
    mental_state = models.CharField(max_length=255, verbose_name='Mental State', blank=True, null=True)
    medications = models.JSONField(verbose_name='Medications', blank=True, null=True)
    care_activities = models.JSONField(verbose_name='Care Activities', blank=True, null=True)
    notes = models.TextField(blank=True, null=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return f'{self.patient.name} - {self.record_date} {self.record_time}'
    
    class Meta:
        verbose_name = 'Care Record'
        verbose_name_plural = 'Care Records'
        ordering = ['-record_date', '-record_time']

class VitalSigns(models.Model):
    """Vital Signs Detail (Legacy/Detailed)"""
    care_record = models.OneToOneField(CareRecord, on_delete=models.CASCADE, primary_key=True, verbose_name='Care Record')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Temperature', null=True, blank=True)
    heart_rate = models.IntegerField(verbose_name='Heart Rate', null=True, blank=True)
    respiratory_rate = models.IntegerField(verbose_name='Respiratory Rate', null=True, blank=True)
    systolic_pressure = models.IntegerField(verbose_name='Systolic Pressure', null=True, blank=True)
    diastolic_pressure = models.IntegerField(verbose_name='Diastolic Pressure', null=True, blank=True)
    blood_oxygen = models.IntegerField(verbose_name='Blood Oxygen', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Vital Signs'
        verbose_name_plural = 'Vital Signs'

class CareTemplate(models.Model):
    """Care Template Model"""
    name = models.CharField(max_length=100, verbose_name='Template Name')
    care_level = models.CharField(max_length=20, verbose_name='Care Level')
    template_content = models.JSONField(verbose_name='Template Content')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='Created By')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Care Template'
        verbose_name_plural = 'Care Templates'

class DailyCareTask(models.Model):
    """Daily Care Task (Simplified Checklist)"""
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='Patient')
    task_date = models.DateField(default=timezone.now, verbose_name='Task Date')
    
    # Checklist fields
    vital_signs_normal = models.BooleanField(default=False, verbose_name='Vital Signs Normal')
    diet_normal = models.BooleanField(default=False, verbose_name='Diet Normal')
    mental_normal = models.BooleanField(default=False, verbose_name='Mental State Normal')
    
    # Metadata
    is_completed = models.BooleanField(default=False, verbose_name='Is Completed')
    last_updated_by = models.ForeignKey('users.StaffUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Last Updated By')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Daily Care Task'
        verbose_name_plural = 'Daily Care Tasks'
        unique_together = ['patient', 'task_date']
        ordering = ['patient__room']

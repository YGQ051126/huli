from django.db import models

class Appointment(models.Model):
    """预约模型"""
    TYPE_CHOICES = (
        ('visit', '探视'),
        ('service', '服务'),
        ('consultation', '咨询'),
    )
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='预约类型')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='院民')
    family_user = models.ForeignKey('users.FamilyUser', on_delete=models.CASCADE, verbose_name='亲属')
    staff_user = models.ForeignKey('users.StaffUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='服务人员')
    date = models.DateField(verbose_name='预约日期')
    time_slot = models.CharField(max_length=20, verbose_name='时间段')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    approved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='审批人')
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name='审批时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.patient.name} - {self.date} {self.time_slot}'
    
    class Meta:
        verbose_name = '预约'
        verbose_name_plural = '预约管理'
        ordering = ['-date', 'time_slot']

class AppointmentTimeSlot(models.Model):
    """预约时间段模型"""
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    is_available = models.BooleanField(default=True, verbose_name='是否可用')
    max_appointments = models.IntegerField(default=1, verbose_name='最大预约数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.start_time} - {self.end_time}'
    
    class Meta:
        verbose_name = '预约时间段'
        verbose_name_plural = '预约时间段管理'

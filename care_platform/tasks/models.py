from django.db import models

class Task(models.Model):
    """任务模型"""
    TASK_TYPE_CHOICES = (
        ('nursing', '护理任务'),
        ('admin', '管理任务'),
        ('service', '服务任务'),
        ('bed_scheduling', '床位调度'),
        ('activity', '活动安排'),
    )
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('in_progress', '处理中'),
        ('completed', '已完成'),
        ('delayed', '已延迟'),
        ('cancelled', '已取消'),
    )
    PRIORITY_CHOICES = (
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    )
    
    type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, verbose_name='任务类型')
    title = models.CharField(max_length=255, verbose_name='任务标题')
    description = models.TextField(verbose_name='任务描述')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.CASCADE, verbose_name='负责人')
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='关联院民')
    due_date = models.DateField(verbose_name='截止日期')
    due_time = models.TimeField(null=True, blank=True, verbose_name='截止时间')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='优先级')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务管理'
        ordering = ['-due_date', '-priority']

class TaskAssignment(models.Model):
    """任务分配模型"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='任务')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.CASCADE, verbose_name='分配人员')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')
    assigned_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='分配人')
    
    def __str__(self):
        return f'{self.task.title} - {self.staff.user.real_name}'
    
    class Meta:
        verbose_name = '任务分配'
        verbose_name_plural = '任务分配管理'

class TaskCompletion(models.Model):
    """任务完成模型"""
    task = models.OneToOneField(Task, on_delete=models.CASCADE, primary_key=True, verbose_name='任务')
    completed_by = models.ForeignKey('users.StaffUser', on_delete=models.CASCADE, verbose_name='完成人')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='完成时间')
    completion_notes = models.TextField(blank=True, null=True, verbose_name='完成备注')
    attached_files = models.JSONField(blank=True, null=True, verbose_name='附件')
    
    def __str__(self):
        return f'{self.task.title} - 已完成'
    
    class Meta:
        verbose_name = '任务完成记录'
        verbose_name_plural = '任务完成管理'

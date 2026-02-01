from django.db import models

class Notification(models.Model):
    """通知模型"""
    NOTIFICATION_TYPE_CHOICES = (
        ('system', '系统通知'),
        ('service', '服务通知'),
        ('health', '健康通知'),
        ('payment', '支付通知'),
        ('appointment', '预约通知'),
        ('task', '任务通知'),
        ('birthday', '生日提醒'),
        ('festival', '节日关怀'),
    )
    STATUS_CHOICES = (
        ('unread', '未读'),
        ('read', '已读'),
    )
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='接收用户')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='通知类型')
    title = models.CharField(max_length=255, verbose_name='通知标题')
    content = models.TextField(verbose_name='通知内容')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread', verbose_name='状态')
    related_id = models.IntegerField(blank=True, null=True, verbose_name='关联ID')
    related_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='关联类型')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    
    def __str__(self):
        return f'{self.title} - {self.user.real_name}'
    
    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知管理'
        ordering = ['-created_at']

class CareReminder(models.Model):
    """关怀提醒模型"""
    REMINDER_TYPE_CHOICES = (
        ('birthday', '生日提醒'),
        ('festival', '节日关怀'),
        ('health', '健康提醒'),
        ('anniversary', '纪念日'),
    )
    
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='院民')
    type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES, verbose_name='提醒类型')
    title = models.CharField(max_length=255, verbose_name='提醒标题')
    content = models.TextField(verbose_name='提醒内容')
    reminder_date = models.DateField(verbose_name='提醒日期')
    is_participated = models.BooleanField(default=False, verbose_name='是否参与')
    participation_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='参与方式')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.patient.name} - {self.type} - {self.reminder_date}'
    
    class Meta:
        verbose_name = '关怀提醒'
        verbose_name_plural = '关怀提醒管理'
        ordering = ['reminder_date']

class ReminderParticipation(models.Model):
    """提醒参与模型"""
    reminder = models.ForeignKey(CareReminder, on_delete=models.CASCADE, verbose_name='关怀提醒')
    family = models.ForeignKey('users.FamilyUser', on_delete=models.CASCADE, verbose_name='参与亲属')
    participation_type = models.CharField(max_length=20, verbose_name='参与方式')
    message = models.TextField(blank=True, null=True, verbose_name='留言内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return f'{self.family.user.real_name} - {self.reminder.title}'
    
    class Meta:
        verbose_name = '提醒参与记录'
        verbose_name_plural = '提醒参与管理'

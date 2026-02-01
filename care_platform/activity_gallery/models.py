from django.db import models

class Activity(models.Model):
    """活动模型"""
    title = models.CharField(max_length=255, verbose_name='活动标题')
    description = models.TextField(verbose_name='活动描述')
    activity_date = models.DateField(verbose_name='活动日期')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上传人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.title} - {self.activity_date}'
    
    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动管理'
        ordering = ['-activity_date']

class ActivityMedia(models.Model):
    """活动媒体模型"""
    MEDIA_TYPE_CHOICES = (
        ('image', '图片'),
        ('video', '视频'),
    )
    
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, verbose_name='媒体类型')
    file_url = models.URLField(verbose_name='文件URL')
    file_path = models.CharField(max_length=500, verbose_name='文件本地路径', blank=True, default='')
    image_path = models.CharField(max_length=500, verbose_name='图片路径', blank=True, default='')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.IntegerField(verbose_name='文件大小（字节）')
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='上传人')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    patients = models.ManyToManyField('patients.Patient', blank=True, verbose_name='参与院民')
    
    def __str__(self):
        return f'{self.activity.title} - {self.media_type} - {self.file_name}'
    
    class Meta:
        verbose_name = '活动媒体'
        verbose_name_plural = '活动媒体管理'

class ActivityParticipant(models.Model):
    """活动参与者模型"""
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='院民')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.SET_NULL, null=True, verbose_name='陪同人员')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return f'{self.patient.name} - {self.activity.title}'
    
    class Meta:
        verbose_name = '活动参与者'
        verbose_name_plural = '活动参与者管理'

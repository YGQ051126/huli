from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    """Announcement Model"""
    TARGET_CHOICES = (
        ('all', 'All'),
        ('family', 'Family'),
        ('staff', 'Staff'),
    )
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('retracted', 'Retracted'),
    )
    
    title = models.CharField(max_length=100, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    target_role = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all', verbose_name='Target Audience')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published', verbose_name='Status')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='Publish Time')
    expire_time = models.DateTimeField(null=True, blank=True, verbose_name='Expire Time')
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name='Creator')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-publish_time']
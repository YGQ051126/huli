from django.db import models

class Message(models.Model):
    """Message model"""
    MESSAGE_TYPE_CHOICES = (
        ('text', 'Text'),
        ('voice', 'Voice'),
        ('image', 'Image'),
        ('system', 'System Message'),
    )
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    )
    
    type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, verbose_name='Message Type')
    sender = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='sent_messages', verbose_name='Sender')
    receiver = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='received_messages', verbose_name='Receiver')
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Related Patient')
    content = models.TextField(verbose_name='Message Content')
    duration = models.IntegerField(blank=True, null=True, verbose_name='Voice Duration (seconds)')
    file_url = models.URLField(blank=True, null=True, verbose_name='File URL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent', verbose_name='Status')
    is_read = models.BooleanField(default=False, verbose_name='Is Read') # type: ignore
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Read At')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        sender_name = getattr(self.sender, 'real_name', 'System') if self.sender else 'System'
        receiver_name = getattr(self.receiver, 'real_name', 'Unknown') if self.receiver else 'Unknown'
        return f'{sender_name} -> {receiver_name} - {self.type}'
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages Management'
        ordering = ['-created_at']

class Conversation(models.Model):
    """Conversation model"""
    participants = models.ManyToManyField('users.User', verbose_name='Participants')
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Related Patient')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Last Message')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    def __str__(self):
        participants = self.participants.all() # type: ignore
        if participants.exists(): # type: ignore
            participants_names = ', '.join([getattr(user, 'real_name', 'Unknown') for user in participants]) # type: ignore
        else:
            participants_names = 'No participants'
        return f'{participants_names}'
    
    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations Management'
        ordering = ['-updated_at']

class Notification(models.Model):
    """Notification model"""
    NOTIFICATION_TYPE_CHOICES = (
        ('system', 'System'),
        ('service', 'Service'),
        ('health', 'Health'),
        ('payment', 'Payment'),
        ('appointment', 'Appointment'),
        ('task', 'Task'),
    )
    STATUS_CHOICES = (
        ('unread', 'Unread'),
        ('read', 'Read'),
    )
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='communication_notifications', verbose_name='Recipient')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='Notification Type')
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread', verbose_name='Status')
    related_id = models.IntegerField(blank=True, null=True, verbose_name='Related ID')
    related_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='Related Type')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Read At')
    
    def __str__(self):
        user_name = getattr(self.user, 'real_name', 'Unknown') if self.user else 'Unknown'
        return f'{self.title} - {user_name}'
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications Management'
        ordering = ['-created_at']

from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    """服务模型"""
    SERVICE_TYPE_CHOICES = (
        ('daily', '日常护理'),
        ('medical', '医疗服务'),
        ('recreation', '娱乐活动'),
        ('custom', '个性化服务'),
        ('consultation', '咨询服务'),
    )
    
    name = models.CharField(max_length=255, verbose_name='服务名称')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, verbose_name='服务类型')
    description = models.TextField(verbose_name='服务描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='服务价格')
    duration = models.IntegerField(blank=True, null=True, verbose_name='服务时长（分钟）')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    # image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name='服务图片') # Uncomment if needed
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '服务'
        verbose_name_plural = '服务管理'

class CustomServiceRequest(models.Model):
    """个性化服务申请模型 (Legacy)"""
    STATUS_CHOICES = (
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    family = models.ForeignKey('users.FamilyUser', on_delete=models.CASCADE, verbose_name='申请人')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='院民')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name='服务类型')
    service_name = models.CharField(max_length=255, verbose_name='服务名称')
    description = models.TextField(verbose_name='服务描述')
    expected_date = models.DateField(verbose_name='期望服务日期')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='服务费用')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    approved_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='审批人')
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name='审批时间')
    feedback = models.TextField(blank=True, null=True, verbose_name='服务反馈')
    rating = models.IntegerField(blank=True, null=True, verbose_name='评分')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.service_name} - {self.patient.name}'
    
    class Meta:
        verbose_name = '个性化服务申请'
        verbose_name_plural = '个性化服务管理'
        ordering = ['-created_at']

class ServiceExecution(models.Model):
    """服务执行模型 (Legacy)"""
    custom_service = models.OneToOneField(CustomServiceRequest, on_delete=models.CASCADE, primary_key=True, verbose_name='个性化服务')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.CASCADE, verbose_name='服务人员')
    execution_date = models.DateField(verbose_name='执行日期')
    start_time = models.TimeField(verbose_name='开始时间')
    end_time = models.TimeField(verbose_name='结束时间')
    notes = models.TextField(blank=True, null=True, verbose_name='执行备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.custom_service.service_name} - {self.execution_date}'
    
    class Meta:
        verbose_name = '服务执行记录'
        verbose_name_plural = '服务执行管理'

# --- New Models for Personalized Service Feature ---

class ServiceOrder(models.Model):
    """Service Order Model"""
    STATUS_CHOICES = (
        ('pending', 'Pending Staff'), 
        ('processing', 'Processing'),
        ('completed', 'Completed'), 
        ('rated', 'Rated'),
        ('cancelled', 'Cancelled'),
    )
    
    order_no = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    family = models.ForeignKey('users.FamilyUser', on_delete=models.CASCADE, verbose_name='亲属')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='服务对象')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    note = models.TextField(blank=True, null=True, verbose_name='备注')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='服务人员')
    
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.order_no
        
    class Meta:
        verbose_name = '服务订单'
        verbose_name_plural = '服务订单'
        ordering = ['-created_at']

class ServiceOrderItem(models.Model):
    """订单明细"""
    order = models.ForeignKey(ServiceOrder, related_name='items', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    service_name = models.CharField(max_length=255, verbose_name='服务名称') 
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    
    def __str__(self):
        return f"{self.order.order_no} - {self.service_name}"

class ServiceFeedback(models.Model):
    """服务反馈（员工填写）"""
    order = models.OneToOneField(ServiceOrder, on_delete=models.CASCADE, related_name='feedback', verbose_name='订单')
    staff = models.ForeignKey('users.StaffUser', on_delete=models.CASCADE, verbose_name='服务人员', null=True, blank=True)
    content = models.TextField(verbose_name='反馈内容')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '服务反馈'
        verbose_name_plural = '服务反馈'

class ServiceFeedbackImage(models.Model):
    """反馈图片"""
    feedback = models.ForeignKey(ServiceFeedback, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='feedback_images/', verbose_name='图片')
    created_at = models.DateTimeField(auto_now_add=True)

class ServiceReview(models.Model):
    """服务评价（家属填写）"""
    order = models.OneToOneField(ServiceOrder, on_delete=models.CASCADE, related_name='review', verbose_name='订单')
    rating = models.IntegerField(verbose_name='评分', choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name='评价内容', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '服务评价'
        verbose_name_plural = '服务评价'

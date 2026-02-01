from decimal import Decimal
from django.db import models

class Bill(models.Model):
    """账单模型"""
    BILL_TYPE_CHOICES = (
        ('monthly', '月度账单'),
        ('service', '服务账单'),
        ('deposit', '押金'),
        ('other', '其他费用'),
    )
    STATUS_CHOICES = (
        ('unpaid', '未支付'),
        ('paid', '已支付'),
        ('partially_paid', '部分支付'),
    )
    
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, verbose_name='院民')
    family = models.ForeignKey('users.FamilyUser', on_delete=models.SET_NULL, null=True, verbose_name='关联亲属')
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES, verbose_name='账单类型')
    month = models.CharField(max_length=7, verbose_name='账单月份')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='已支付金额')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid', verbose_name='状态')
    due_date = models.DateField(verbose_name='到期日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.patient.name} - {self.bill_type} - {self.month}'
    
    class Meta:
        verbose_name = '账单'
        verbose_name_plural = '账单管理'
        ordering = ['-month']

class BillItem(models.Model):
    """账单明细模型"""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, verbose_name='账单')
    item_name = models.CharField(max_length=255, verbose_name='项目名称')
    description = models.TextField(blank=True, null=True, verbose_name='项目描述')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.bill.patient.name} - {self.item_name}'
    
    class Meta:
        verbose_name = '账单明细'
        verbose_name_plural = '账单明细管理'

class Payment(models.Model):
    """支付模型"""
    PAYMENT_METHOD_CHOICES = (
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行转账'),
        ('cash', '现金'),
        ('balance', '余额支付'),
        ('other', '其他'),
    )
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('success', '成功'),
        ('failed', '失败'),
        ('refunded', '已退款'),
    )
    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, verbose_name='关联账单')
    family = models.ForeignKey('users.FamilyUser', on_delete=models.SET_NULL, null=True, verbose_name='支付人')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='支付方式')
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name='交易ID')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    notes = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return f'{self.bill.patient.name} - {self.amount} - {self.status}'
    
    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录管理'
        ordering = ['-paid_at']

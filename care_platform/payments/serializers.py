from rest_framework import serializers
from .models import Bill, BillItem, Payment
from patients.serializers import PatientSerializer
from users.serializers import FamilyUserSerializer

class BillItemSerializer(serializers.ModelSerializer):
    """账单明细序列化器"""
    
    class Meta:
        model = BillItem
        fields = ['id', 'item_name', 'description', 'quantity', 'unit_price', 'amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BillSerializer(serializers.ModelSerializer):
    """账单序列化器"""
    patient = PatientSerializer(read_only=True)
    family = FamilyUserSerializer(read_only=True)
    items = BillItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Bill
        fields = ['id', 'patient', 'family', 'bill_type', 'month', 'total_amount', 'paid_amount', 'status', 'due_date', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class BillCreateSerializer(serializers.ModelSerializer):
    """账单创建序列化器"""
    items = BillItemSerializer(many=True, required=True)
    
    class Meta:
        model = Bill
        fields = ['patient', 'family', 'bill_type', 'month', 'total_amount', 'status', 'due_date', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        bill = Bill.objects.create(**validated_data)
        
        for item_data in items_data:
            BillItem.objects.create(bill=bill, **item_data)
        
        return bill

class BillUpdateSerializer(serializers.ModelSerializer):
    """账单更新序列化器"""
    items = BillItemSerializer(many=True, required=False)
    
    class Meta:
        model = Bill
        fields = ['status', 'paid_amount', 'items']
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        # 更新账单基本信息
        instance = super().update(instance, validated_data)
        
        # 如果提供了新的账单明细，先删除旧的，再创建新的
        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                BillItem.objects.create(bill=instance, **item_data)
        
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    """支付记录序列化器"""
    bill = BillSerializer(read_only=True)
    family = FamilyUserSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'bill', 'family', 'amount', 'payment_method', 'transaction_id', 'status', 'paid_at', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PaymentCreateSerializer(serializers.ModelSerializer):
    """支付记录创建序列化器"""
    
    class Meta:
        model = Payment
        fields = ['bill', 'family', 'amount', 'payment_method', 'transaction_id', 'notes']
    
    def create(self, validated_data):
        # 创建支付记录
        payment = Payment.objects.create(**validated_data)
        
        # 更新账单状态
        bill = payment.bill
        bill.paid_amount += payment.amount
        
        if bill.paid_amount >= bill.total_amount:
            bill.status = 'paid'
        elif bill.paid_amount > 0:
            bill.status = 'partially_paid'
        else:
            bill.status = 'unpaid'
        
        bill.save()
        
        return payment

class PaymentUpdateSerializer(serializers.ModelSerializer):
    """支付记录更新序列化器"""
    
    class Meta:
        model = Payment
        fields = ['status', 'paid_at', 'notes']

class BillStatusUpdateSerializer(serializers.ModelSerializer):
    """账单状态更新序列化器"""
    
    class Meta:
        model = Bill
        fields = ['status']

class PaymentMethodSerializer(serializers.Serializer):
    """支付方式序列化器"""
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    bill_id = serializers.IntegerField()

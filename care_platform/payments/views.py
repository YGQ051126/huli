from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from utils.permissions import IsAdminUser, IsStaffUser, IsFamilyUser
from utils.response import success_response, error_response
from .models import Bill, BillItem, Payment
from .serializers import (
    BillSerializer,
    BillCreateSerializer,
    BillUpdateSerializer,
    BillStatusUpdateSerializer,
    BillItemSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentUpdateSerializer,
    PaymentMethodSerializer
)
from datetime import datetime, date
import uuid
import csv
from django.http import HttpResponse
from django.db.models import Sum, Count, Q
from rest_framework.views import APIView

class BillViewSet(viewsets.ModelViewSet):
    """Bill view set"""
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    
    def get_permissions(self):
        """Get permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Get serializer class based on action"""
        if self.action == 'create':
            return BillCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BillUpdateSerializer
        return BillSerializer
    
    def create(self, request, *args, **kwargs):
        """Create bill"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        
        return success_response(
            BillSerializer(bill).data,
            code=201,
            message='Bill created successfully'
        )
    
    def update(self, request, *args, **kwargs):
        """Update bill"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        
        return success_response(
            BillSerializer(bill).data,
            message='Bill updated successfully'
        )

class FamilyBillListView(generics.ListAPIView):
    """Get bill list for family users"""
    serializer_class = BillSerializer
    permission_classes = [IsFamilyUser]
    
    def get_queryset(self):
        """Get bills for current family user"""
        family_user = getattr(self.request.user, 'familyuser', None)
        if not family_user:
            return Bill.objects.none()
        return Bill.objects.filter(patient=family_user.patient).order_by('-month', '-created_at')

class RefreshBillsView(APIView):
    """
    Refresh monthly bills manually.
    Generates bills for the current month if they don't exist.
    """
    permission_classes = [IsAuthenticated] # Could be strictly IsFamilyUser or IsAdminUser

    def post(self, request):
        user = request.user
        # Assuming only family users trigger this for their own patient for now
        # Or admin triggers for all. 
        # Requirement: "Manual refresh button... call /api/bills/refresh"
        
        current_month = datetime.now().strftime('%Y-%m')
        
        target_patients = []
        if hasattr(user, 'familyuser'):
            target_patients.append(user.familyuser.patient)
        elif user.role == 'admin':
            # Admin might want to refresh all or specific? 
            # For simplicity, if admin, maybe pass patient_id or refresh all.
            # Let's stick to family user context from the prompt's UI description.
            pass
        
        created_count = 0
        for patient in target_patients:
            # Check if monthly bill exists
            exists = Bill.objects.filter(
                patient=patient, 
                month=current_month, 
                bill_type='monthly'
            ).exists()
            
            if not exists:
                # Create Mock Monthly Bill
                # In real app, calculate from bed price + service levels
                # Here we mock it.
                Bill.objects.create(
                    patient=patient,
                    family=patient.familyuser_set.first(), # Assign to first family user found
                    bill_type='monthly',
                    month=current_month,
                    total_amount=5000.00, # Mock amount
                    due_date=datetime.now().date().replace(day=28), # Due end of month
                    status='unpaid'
                )
                created_count += 1
                
        return success_response({
            'created': created_count,
            'month': current_month
        }, message='Bills refreshed successfully')

class BulkPaymentCreateView(APIView):
    """
    Create payment for multiple bills.
    Directly processes payment without cashier URL redirection (Mock).
    """
    permission_classes = [IsFamilyUser]

    def post(self, request):
        bill_ids = request.data.get('bill_ids', [])
        if not bill_ids:
            return error_response(message="No bills selected", code=400)
            
        family_user = request.user.familyuser
        bills = Bill.objects.filter(id__in=bill_ids, patient=family_user.patient, status__in=['unpaid', 'partially_paid'])
        
        if len(bills) != len(set(bill_ids)):
             # Some bills might be invalid or paid or not belong to user
             pass 

        total_amount = sum(bill.total_amount - bill.paid_amount for bill in bills)
        
        if total_amount <= 0:
            return error_response(message="Invalid total amount", code=400)
            
        transaction_id = f'PAY{uuid.uuid4().hex[:12].upper()}'
        
        payment_ids = []
        for bill in bills:
            amount_to_pay = bill.total_amount - bill.paid_amount
            p = Payment.objects.create(
                bill=bill,
                family=family_user,
                amount=amount_to_pay,
                payment_method='online', # default
                transaction_id=f"{transaction_id}_{bill.id}", # Unique per record # type: ignore
                status='success', # Directly mark as success
                paid_at=datetime.now(),
                notes=f"Bulk payment group {transaction_id}"
            )
            
            # Update Bill Status
            bill.paid_amount = bill.total_amount
            bill.status = 'paid'
            bill.save()
            
            payment_ids.append(p.id) # type: ignore
            
        return success_response({
            'order_id': transaction_id,
            'total_amount': total_amount,
            'status': 'success'
        }, message='Payment successful')

class AdminBillExportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        month = request.query_params.get('month')
        bill_type = request.query_params.get('type')
        status = request.query_params.get('status')
        
        queryset = Bill.objects.all()
        if month:
            queryset = queryset.filter(month=month)
        if bill_type:
            queryset = queryset.filter(bill_type=bill_type)
        if status:
            queryset = queryset.filter(status=status)
            
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="bills_export_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Patient', 'Month', 'Type', 'Amount', 'Status', 'Created At'])
        
        for bill in queryset:
            writer.writerow([
                bill.id, # type: ignore
                bill.patient.name,
                bill.month,
                bill.get_bill_type_display(), # type: ignore
                bill.total_amount,
                bill.get_status_display(), # type: ignore
                bill.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
            
        return response

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Monthly Income Trend (Last 6 months)
        # Arrears Stats
        # Payment Rate
        
        total_bills = Bill.objects.count()
        paid_bills = Bill.objects.filter(status='paid').count()
        payment_rate = (paid_bills / total_bills * 100) if total_bills > 0 else 0
        
        total_arrears = Bill.objects.filter(status='unpaid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        return success_response({
            'payment_rate': round(payment_rate, 2),
            'total_arrears': total_arrears,
            # Mock trend data for now
            'income_trend': [
                {'month': '2025-08', 'amount': 12000},
                {'month': '2025-09', 'amount': 15000},
                {'month': '2025-10', 'amount': 18000},
                {'month': '2025-11', 'amount': 14000},
                {'month': '2025-12', 'amount': 20000},
                {'month': '2026-01', 'amount': 22000},
            ]
        })

class FamilyBillDetailView(generics.RetrieveAPIView):
    """Get bill detail for family users"""
    serializer_class = BillSerializer
    permission_classes = [IsFamilyUser]
    
    def get_queryset(self):
        """Get bills for current family user"""
        family_user = getattr(self.request.user, 'familyuser', None)
        if not family_user:
            return Bill.objects.none()
        return Bill.objects.filter(patient=family_user.patient)

class MonthlyBillView(generics.RetrieveAPIView):
    """Get monthly bill detail"""
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Get bill by patient id and month"""
        patient_id = self.kwargs.get('patient_id')
        month = self.kwargs.get('month')
        
        user = self.request.user
        role = getattr(user, 'role', None)

        # Verify permission: only admin, staff or family can query
        if role == 'admin' or role == 'staff':
            bill = Bill.objects.get(patient_id=patient_id, month=month)
        elif role == 'family':
            # Family can only query bills for their associated patient
            family_user = getattr(user, 'familyuser', None)
            if not family_user:
                raise PermissionDenied("No family user profile found")
            bill = Bill.objects.get(patient_id=family_user.patient.id, month=month)
        else:
            raise PermissionDenied("No permission to access this bill")
        
        return bill

class PaymentViewSet(viewsets.ModelViewSet):
    """Payment view set"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_permissions(self):
        """Get permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Get serializer class based on action"""
        if self.action == 'create':
            return PaymentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PaymentUpdateSerializer
        return PaymentSerializer
    
    def create(self, request, *args, **kwargs):
        """Create payment"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        return success_response(
            PaymentSerializer(payment).data,
            code=201,
            message='Payment created successfully'
        )

class OnlinePaymentView(generics.GenericAPIView):
    """Online payment view (mock payment)"""
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsFamilyUser]
    
    def post(self, request):
        """Process online payment"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment_method = serializer.validated_data['payment_method']
        amount = serializer.validated_data['amount']
        bill_id = serializer.validated_data['bill_id']
        
        try:
            # Get bill
            bill = Bill.objects.get(id=bill_id)
            family_user = request.user.familyuser
            
            # Verify bill ownership
            if bill.patient != family_user.patient:
                return error_response(code=403, message='No permission to pay this bill')
            
            # Check balance
            if family_user.balance < amount:
                return error_response(code=400, message='Insufficient balance')
            
            # Mock payment logic: directly create payment record and update bill status
            transaction_id = f'PAY{uuid.uuid4().hex[:12].upper()}'
            
            # Deduct balance
            family_user.balance -= amount
            family_user.save()
            
            # Create payment record
            payment = Payment.objects.create(
                bill=bill,
                family=family_user,
                amount=amount,
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='success',
                paid_at=datetime.now()
            )
            
            # Update bill status
            bill.paid_amount += amount
            if bill.paid_amount >= bill.total_amount:
                bill.status = 'paid'
            elif bill.paid_amount > 0:
                bill.status = 'partially_paid'
            bill.save()
            
            return success_response(
                PaymentSerializer(payment).data,
                message='Payment successful'
            )
        except Bill.DoesNotExist:
            return error_response(code=404, message='Bill not found')
        except Exception as e:
            return error_response(code=500, message=f'Payment failed: {str(e)}')

class BillPayView(generics.GenericAPIView):
    """Pay bill via URL param"""
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsFamilyUser]

    def post(self, request, pk):
        """Process online payment with bill_id from URL"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment_method = serializer.validated_data['payment_method']
        amount = serializer.validated_data['amount']
        bill_id = pk # Get from URL
        
        try:
            # Get bill
            bill = Bill.objects.get(id=bill_id)
            family_user = request.user.familyuser
            
            # Verify bill ownership
            if bill.patient != family_user.patient:
                return error_response(code=403, message='No permission to pay this bill')
            
            # Check balance
            if family_user.balance < amount:
                return error_response(code=400, message='Insufficient balance')
            
            # Mock payment logic
            transaction_id = f'PAY{uuid.uuid4().hex[:12].upper()}'
            
            # Deduct balance
            family_user.balance -= amount
            family_user.save()
            
            # Create payment record
            payment = Payment.objects.create(
                bill=bill,
                family=family_user,
                amount=amount,
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='success',
                paid_at=datetime.now()
            )
            
            # Update bill status
            bill.paid_amount += amount
            if bill.paid_amount >= bill.total_amount:
                bill.status = 'paid'
            elif bill.paid_amount > 0:
                bill.status = 'partially_paid'
            bill.save()
            
            return success_response(
                PaymentSerializer(payment).data,
                message='Payment successful'
            )
        except Bill.DoesNotExist:
            return error_response(code=404, message='Bill not found')
        except Exception as e:
            return error_response(code=500, message=f'Payment failed: {str(e)}')

class BillStatusUpdateView(generics.GenericAPIView):
    """Bill status update view"""
    serializer_class = BillStatusUpdateSerializer
    permission_classes = [IsAdminUser]
    
    def put(self, request, pk):
        """Update bill status"""
        bill = Bill.objects.get(id=pk)
        serializer = self.get_serializer(bill, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        
        return success_response(
            BillSerializer(bill).data,
            message='Bill status updated successfully'
        )

class PaymentHistoryView(generics.ListAPIView):
    """Get payment history"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get payment history based on user role"""
        user = self.request.user
        role = getattr(user, 'role', None)
        
        if role == 'admin' or role == 'staff':
            # Admin and staff can view all payment records
            return Payment.objects.all().order_by('-paid_at')
        elif role == 'family':
            # Family can only view their own payment records
            family_user = getattr(user, 'familyuser', None)
            if not family_user:
                return Payment.objects.none()
            return Payment.objects.filter(family=family_user).order_by('-paid_at')
        else:
            return Payment.objects.none()

class FamilyPaymentHistoryView(generics.ListAPIView):
    """Family user payment history"""
    serializer_class = PaymentSerializer
    permission_classes = [IsFamilyUser]
    
    def get_queryset(self):
        """Get payment history for current family user"""
        family_user = getattr(self.request.user, 'familyuser', None)
        if not family_user:
            return Payment.objects.none()
        return Payment.objects.filter(family=family_user).order_by('-paid_at')

class BillByPatientView(generics.ListAPIView):
    """Get bills by patient id"""
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get bills for specific patient"""
        patient_id = self.kwargs.get('patient_id')
        return Bill.objects.filter(patient_id=patient_id).order_by('-month')

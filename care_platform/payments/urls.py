from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BillViewSet,
    PaymentViewSet,
    FamilyBillListView,
    FamilyBillDetailView,
    MonthlyBillView,
    OnlinePaymentView,
    BillStatusUpdateView,
    PaymentHistoryView,
    FamilyPaymentHistoryView,
    BillByPatientView,
    BillPayView,
    RefreshBillsView,
    BulkPaymentCreateView,
    AdminBillExportView,
    AdminDashboardView
)

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    # 亲属端费用查询和支付相关
    path('family/bills/', FamilyBillListView.as_view(), name='family-bills'),
    path('family/bills/<int:pk>/', FamilyBillDetailView.as_view(), name='family-bill-detail'),
    path('family/bills/<int:pk>/pay/', BillPayView.as_view(), name='family-bill-pay'),
    path('family/payments/', FamilyPaymentHistoryView.as_view(), name='family-payments'),
    path('family/payments/online/', OnlinePaymentView.as_view(), name='online-payment'),
    
    # New endpoints
    path('refresh-bills/', RefreshBillsView.as_view(), name='bills-refresh'),
    path('bulk-payments/create/', BulkPaymentCreateView.as_view(), name='payment-create'),
    path('admin/bills/export/', AdminBillExportView.as_view(), name='admin-bill-export'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    
    # 费用查询
    path('bills/patient/<int:patient_id>/', BillByPatientView.as_view(), name='bills-by-patient'),
    path('bills/monthly/<int:patient_id>/<str:month>/', MonthlyBillView.as_view(), name='monthly-bill'),
    
    # 支付历史
    path('payments/history/', PaymentHistoryView.as_view(), name='payment-history'),
    
    # 账单状态更新
    path('bills/<int:pk>/status/', BillStatusUpdateView.as_view(), name='bill-status-update'),
]

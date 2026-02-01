from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonthlyReportView, ApprovalViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'approvals', ApprovalViewSet, basename='approval')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('reports/monthly/', MonthlyReportView.as_view(), name='monthly-report'),
    path('', include(router.urls)),
]

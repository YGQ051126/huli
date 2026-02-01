from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    HealthAssessmentViewSet,
    MedicalRecordViewSet,
    PatientHealthAssessmentsView,
    PatientMedicalRecordsView,
    FamilyPatientListView,
    FamilyPatientDetailView,
    FamilyDashboardView
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'health-assessments', HealthAssessmentViewSet, basename='health-assessment')
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')

urlpatterns = [
    path('patients/family/dashboard/', FamilyDashboardView.as_view(), name='family-dashboard'),
    path('patients/<int:patient_id>/health-assessments/', PatientHealthAssessmentsView.as_view(), name='patient-health-assessments'),
    path('patients/<int:patient_id>/medical-records/', PatientMedicalRecordsView.as_view(), name='patient-medical-records'),
    path('family/patients/', FamilyPatientListView.as_view(), name='family-patients'),
    path('family/patients/<int:pk>/', FamilyPatientDetailView.as_view(), name='family-patient-detail'),
    path('', include(router.urls)),
]

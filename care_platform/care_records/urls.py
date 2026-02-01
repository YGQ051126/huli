# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CareRecordViewSet,
    PatientCareRecordsView,
    StaffCareRecordsView,
    FamilyCareRecordsView,
    CareTemplateViewSet,
    ActiveCareTemplatesView,
    CareTemplateByLevelView,
    CareTemplateByPatientView,
    VitalSignsViewSet,
    DailyCareTaskViewSet
)

router = DefaultRouter()
router.register(r'care-records', CareRecordViewSet, basename='care-record')
router.register(r'care-templates', CareTemplateViewSet, basename='care-template')
router.register(r'vital-signs', VitalSignsViewSet, basename='vital-sign')
router.register(r'daily-care-tasks', DailyCareTaskViewSet, basename='daily-care-task')

urlpatterns = [
    # Staff Frontend Routes Support
    path('staff/health/<int:patient_id>/overview', PatientCareRecordsView.as_view(), name='staff-health-overview'),
    path('staff/care-records/template', CareTemplateByPatientView.as_view(), name='staff-care-template'),
    path('staff/care-records/submit', CareRecordViewSet.as_view({'post': 'submit'}), name='staff-care-record-submit'),
    path('staff/care-records', CareRecordViewSet.as_view({'post': 'create'}), name='staff-care-record-create'),

    path('', include(router.urls)),
    path('patients/<int:patient_id>/care-records/', PatientCareRecordsView.as_view(), name='patient-care-records'),
    path('staff/<int:staff_id>/care-records/', StaffCareRecordsView.as_view(), name='staff-care-records'),
    path('family/care-records/', FamilyCareRecordsView.as_view(), name='family-care-records'),
    path('active-care-templates/', ActiveCareTemplatesView.as_view(), name='active-care-templates'),
    path('care-templates/level/<str:care_level>/', CareTemplateByLevelView.as_view(), name='care-templates-by-level'),
]

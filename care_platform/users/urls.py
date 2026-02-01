from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    UserLoginView, 
    UserRegisterView, 
    UserProfileView,
    FamilyUserViewSet,
    FamilyRegisterView,
    FamilyUserListByPatientView,
    StaffUserViewSet,
    StaffRegisterView,
    DashboardView,
    LeaveRequestViewSet,
    RelatedStaffView,
    RegisterApplicationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'family-users', FamilyUserViewSet, basename='family-user')
router.register(r'staff-users', StaffUserViewSet, basename='staff-user')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register(r'register-applications', RegisterApplicationViewSet, basename='register-application')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/register/family/', FamilyRegisterView.as_view(), name='family-register'),
    path('auth/register/staff/', StaffRegisterView.as_view(), name='staff-register'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('staff/dashboard/', DashboardView.as_view(), name='staff-dashboard'),
    path('patients/<int:patient_id>/family-users/', FamilyUserListByPatientView.as_view(), name='patient-family-users'),
    path('family/related-staff/', RelatedStaffView.as_view(), name='related-staff'),
]

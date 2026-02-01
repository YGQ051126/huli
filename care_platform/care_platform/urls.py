from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

from patients.views import PatientViewSet, FamilyPatientListView, FamilyPatientDetailView
from users.views import StaffUserViewSet
from appointments.views import AppointmentViewSet, AppointmentCancelView
from users.views import UserLoginView
from payments.views import FamilyBillListView, BillPayView

# Router for aliased routes (e.g. admin/elderly mapping to PatientViewSet)
alias_router = DefaultRouter()
alias_router.register(r'admin/elderly', PatientViewSet, basename='admin-elderly')
alias_router.register(r'admin/staff', StaffUserViewSet, basename='admin-staff')
alias_router.register(r'elderly', PatientViewSet, basename='elderly-alias')

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- V1 API ---
    
    # Auth & Users (includes /auth/login, /users/, etc.)
    path('api/v1/', include('users.urls')),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Legacy alias without version to avoid 404 from older frontend bundles
    path('api/auth/login/', UserLoginView.as_view(), name='user-login-legacy'),
    
    # Admin Panel (Reports)
    path('api/v1/admin/', include('admin_panel.urls')),
    
    # Aliased Admin Routes
    path('api/v1/', include(alias_router.urls)),
    
    # family API Specifics
    path('api/v1/family/elderly/', FamilyPatientListView.as_view(), name='family-elderly-list'),
    path('api/v1/family/elderly/<int:pk>/', FamilyPatientDetailView.as_view(), name='family-elderly-detail'),
    
    # family Appointments (List/Create)
    path('api/v1/family/appointments/', AppointmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='family-appointments'),
    # family Appointment Cancel
    path('api/v1/family/appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='family-appointment-cancel'),
    
    # family Bills and Pay routes are now included via payments.urls
    
    # Standard Apps Includes (providing /patients/, /appointments/ base routes)
    path('api/v1/', include('rooms.urls')),  # ÓÅÏÈ¼ÓÔØrooms£¬±ÜÃâRoomViewSet³åÍ»
    path('api/v1/', include('patients.urls')),
    path('api/v1/', include('appointments.urls')),
    path('api/v1/', include('care_records.urls')),
    path('api/v1/', include('tasks.urls')),
    path('api/v1/', include('communication.urls')),
    path('api/v1/', include('payments.urls')),
    path('api/v1/', include('services.urls')),
    path('api/v1/bed_scheduling/', include('bed_scheduling.urls')),
    path('api/v1/', include('activity_gallery.urls')),
    path('api/v1/', include('notifications.urls')),
    path('api/v1/', include('announcements.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

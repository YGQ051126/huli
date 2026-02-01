from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet,
    AppointmentApproveView,
    AppointmentCancelView,
    AppointmentTimeSlotViewSet,
    AvailableTimeSlotsView,
    PatientAppointmentsView,
    FamilyAppointmentsView,
    StaffAppointmentsView,
    PendingAppointmentsView
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'appointment-slots', AppointmentTimeSlotViewSet, basename='appointment-slot')

urlpatterns = [
    path('', include(router.urls)),
    path('appointments/<int:pk>/approve/', AppointmentApproveView.as_view(), name='appointment-approve'),
    path('appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
    path('available-slots/', AvailableTimeSlotsView.as_view(), name='available-slots'),
    path('patients/<int:patient_id>/appointments/', PatientAppointmentsView.as_view(), name='patient-appointments'),
    path('family/appointments/', FamilyAppointmentsView.as_view(), name='family-appointments'),
    path('staff/appointments/', StaffAppointmentsView.as_view(), name='staff-appointments'),
    path('pending-appointments/', PendingAppointmentsView.as_view(), name='pending-appointments'),
]
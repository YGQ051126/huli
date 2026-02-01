from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet)
router.register(r'care-reminders', views.CareReminderViewSet)
router.register(r'reminder-participations', views.ReminderParticipationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activities', views.ActivityViewSet)
router.register(r'media', views.ActivityMediaViewSet)
router.register(r'participants', views.ActivityParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

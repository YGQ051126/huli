from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'custom-services', views.CustomServiceViewSet)
router.register(r'service-types', views.ServiceTypeViewSet)
router.register(r'service-applications', views.ServiceApplicationViewSet)
router.register(r'service-orders', views.ServiceOrderViewSet, basename='service-order')

urlpatterns = [
    path('', include(router.urls)),
]

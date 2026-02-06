from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register(r'rooms', views.RoomViewSet)
# router.register(r'beds', views.BedViewSet, basename='bed')
# router.register(r'assignments', views.BedAssignmentViewSet)
# router.register(r'cleaning-requests', views.CleaningRequestViewSet)

urlpatterns = [
    # Explicitly define BedViewSet URLs to avoid router issues
    path('beds/', views.BedViewSet.as_view({'get': 'list'}), name='bed-list'),
    path('beds', views.BedViewSet.as_view({'get': 'list'})),
    
    path('beds/status/', views.BedViewSet.as_view({'get': 'status'}), name='bed-status'),
    path('beds/status', views.BedViewSet.as_view({'get': 'status'})),
    
    path('beds/match/', views.BedViewSet.as_view({'post': 'match'}), name='bed-match'),
    path('beds/match', views.BedViewSet.as_view({'post': 'match'})),
    
    path('assignments/', views.BedAssignmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='bed-assignment-list'),
    path('assignments', views.BedAssignmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    
    # Add form download URL
    path('assignments/<str:pk>/form/', views.BedAssignmentViewSet.as_view({'get': 'form'}), name='bed-assignment-form'),
    path('assignments/<str:pk>/form', views.BedAssignmentViewSet.as_view({'get': 'form'})),
    
    path('beds/<str:id>/set_status/', views.BedViewSet.as_view({'patch': 'set_status'}), name='bed-set-status'),
    path('beds/<str:id>/set_status', views.BedViewSet.as_view({'patch': 'set_status'})),
    
    path('', include(router.urls)),
]

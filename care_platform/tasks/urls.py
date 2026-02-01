from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, StaffTaskListView, TaskCompleteView, TaskDelayView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('staff/<int:staff_id>/tasks/', StaffTaskListView.as_view(), name='staff-tasks'),
    
    path('tasks/<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
    path('tasks/<int:pk>/complete', TaskCompleteView.as_view()),
    
    path('tasks/<int:pk>/delay/', TaskDelayView.as_view(), name='task-delay'),
    path('tasks/<int:pk>/delay', TaskDelayView.as_view()),
]
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsAdminUser, IsStaffUser
from utils.response import success_response, error_response
from .models import Task, TaskAssignment, TaskCompletion
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskStatusUpdateSerializer,
    TaskCompleteRequestSerializer,
    TaskDelayRequestSerializer
)
from datetime import datetime

class TaskViewSet(viewsets.ModelViewSet):
    """Task view set"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """Custom queryset to filter by staffId"""
        qs = super().get_queryset()
        staff_id = self.request.query_params.get('staffId')
        if staff_id:
            qs = qs.filter(staff_id=staff_id)
        return qs.order_by('-priority', '-due_date')

    def get_permissions(self):
        """Get permissions based on action"""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Get serializer class based on action"""
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def create(self, request, *args, **kwargs):
        """Create task"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        # Create task assignment record
        TaskAssignment.objects.create(
            task=task,
            staff=task.staff,
            assigned_by=request.user
        )
        
        return success_response(
            TaskSerializer(task).data,
            code=201,
            message='Task created successfully'
        )
    
    def update(self, request, *args, **kwargs):
        """Update task"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        return success_response(
            TaskSerializer(task).data,
            message='Task updated successfully'
        )

class StaffTaskListView(generics.ListAPIView):
    """Get task list for specific staff"""
    serializer_class = TaskSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        """Get tasks for specific staff"""
        staff_id = self.kwargs['staff_id']
        return Task.objects.filter(staff_id=staff_id).order_by('-priority', '-due_date')

class CurrentStaffTasksView(generics.ListAPIView):
    """Get task list for current staff"""
    serializer_class = TaskSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        """Get tasks for current staff"""
        if not hasattr(self.request.user, 'staffuser'):
            return Task.objects.none()
        staff_user = getattr(self.request.user, 'staffuser', None)
        if not staff_user:
            return Task.objects.none()
        return Task.objects.filter(staff=staff_user).order_by('-priority', '-due_date')

class TaskCompleteView(generics.GenericAPIView):
    """Complete task view"""
    queryset = Task.objects.all()
    serializer_class = TaskCompleteRequestSerializer
    permission_classes = [IsStaffUser]
    
    def post(self, request, pk):
        """Complete task"""
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify task ownership
        staff_user = getattr(request.user, 'staffuser', None)
        if not staff_user or task.staff != staff_user:
            return error_response(code=403, message='No permission to complete this task')
        
        # Update task status
        task.status = 'completed'
        task.completed_at = datetime.now()
        task.save()
        
        # Create task completion record
        completion_notes = serializer.validated_data.get('completion_notes', '')
        attached_files = serializer.validated_data.get('attached_files', None)
        
        TaskCompletion.objects.create(
            task=task,
            completed_by=staff_user,
            completion_notes=completion_notes,
            attached_files=attached_files
        )
        
        return success_response(
            TaskSerializer(task).data,
            message='Task completed successfully'
        )

class TaskDelayView(generics.GenericAPIView):
    """Delay task view"""
    queryset = Task.objects.all()
    serializer_class = TaskDelayRequestSerializer
    permission_classes = [IsStaffUser]
    
    def post(self, request, pk):
        """Delay task"""
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify task ownership
        staff_user = getattr(request.user, 'staffuser', None)
        if not staff_user or task.staff != staff_user:
            return error_response(code=403, message='No permission to delay this task')
        
        # Update task status and due date
        task.status = 'delayed'
        task.due_date = serializer.validated_data['new_due_date']
        if 'new_due_time' in serializer.validated_data:
            task.due_time = serializer.validated_data['new_due_time']
        task.save()
        
        return success_response(
            TaskSerializer(task).data,
            message='Task delayed successfully'
        )

class PendingTasksView(generics.ListAPIView):
    """Get pending tasks"""
    serializer_class = TaskSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        """Get pending tasks"""
        return Task.objects.filter(status='pending').order_by('-priority', '-due_date')

class InProgressTasksView(generics.ListAPIView):
    """Get in progress tasks"""
    serializer_class = TaskSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        """Get in progress tasks"""
        return Task.objects.filter(status='in_progress').order_by('-priority', '-due_date')

class CompletedTasksView(generics.ListAPIView):
    """Get completed tasks"""
    serializer_class = TaskSerializer
    permission_classes = [IsStaffUser]
    
    def get_queryset(self):
        """Get completed tasks"""
        return Task.objects.filter(status='completed').order_by('-completed_at')

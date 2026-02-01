from rest_framework import serializers
from .models import Task, TaskAssignment, TaskCompletion
from users.serializers import StaffUserSerializer, UserSerializer
from patients.serializers import PatientSerializer

class TaskSerializer(serializers.ModelSerializer):
    """任务序列化器"""
    staff = StaffUserSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'type', 'title', 'description', 'staff', 'patient', 'due_date', 'due_time', 'status', 'priority', 'completed_at', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    """任务创建序列化器"""
    
    class Meta:
        model = Task
        fields = ['type', 'title', 'description', 'staff', 'patient', 'due_date', 'due_time', 'status', 'priority']

class TaskUpdateSerializer(serializers.ModelSerializer):
    """任务更新序列化器"""
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'staff', 'patient', 'due_date', 'due_time', 'status', 'priority']

class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    """任务状态更新序列化器"""
    
    class Meta:
        model = Task
        fields = ['status']

class TaskAssignmentSerializer(serializers.ModelSerializer):
    """任务分配序列化器"""
    task = TaskSerializer(read_only=True)
    staff = StaffUserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    
    class Meta:
        model = TaskAssignment
        fields = ['id', 'task', 'staff', 'assigned_at', 'assigned_by']
        read_only_fields = ['id', 'assigned_at', 'assigned_by']

class TaskCompletionSerializer(serializers.ModelSerializer):
    """任务完成序列化器"""
    task = TaskSerializer(read_only=True)
    completed_by = StaffUserSerializer(read_only=True)
    
    class Meta:
        model = TaskCompletion
        fields = ['id', 'task', 'completed_by', 'completed_at', 'completion_notes', 'attached_files']
        read_only_fields = ['id', 'completed_at']

class TaskCompleteRequestSerializer(serializers.ModelSerializer):
    """任务完成请求序列化器"""
    completion_notes = serializers.CharField(required=False)
    attached_files = serializers.JSONField(required=False)
    
    class Meta:
        model = TaskCompletion
        fields = ['completion_notes', 'attached_files']

class TaskDelayRequestSerializer(serializers.Serializer):
    """任务延迟请求序列化器"""
    reason = serializers.CharField(required=True)
    new_due_date = serializers.DateField(required=True)
    new_due_time = serializers.TimeField(required=False)

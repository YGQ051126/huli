from rest_framework import permissions
from users.models import User

class IsAdminUser(permissions.BasePermission):
    """只允许管理员访问"""
    def has_permission(self, request, view):
        # 确保request.user存在且有role属性
        return hasattr(request.user, 'role') and request.user.role == 'admin'

class IsStaffUser(permissions.BasePermission):
    """只允许工作人员访问"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'staff'

class IsFamilyUser(permissions.BasePermission):
    """只允许亲属用户访问"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'family'

class IsSelfOrAdmin(permissions.BasePermission):
    """只允许用户访问自己的资源或管理员访问"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user or (hasattr(request.user, 'role') and request.user.role == 'admin')

class IsFamilyOfPatient(permissions.BasePermission):
    """只允许患者的亲属访问相关资源"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'family'
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'patient'):
            return hasattr(request.user, 'familyuser') and hasattr(request.user.familyuser, 'patient') and obj.patient == request.user.familyuser.patient
        elif hasattr(obj, 'family'):
            return obj.family.user == request.user
        return False

class IsStaffOrAdmin(permissions.BasePermission):
    """只允许工作人员或管理员访问"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and (request.user.role == 'staff' or request.user.role == 'admin')

class IsAssignedStaff(permissions.BasePermission):
    """只允许被分配的工作人员访问"""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'staff'):
            return obj.staff.user == request.user or (hasattr(request.user, 'role') and request.user.role == 'admin')
        return False
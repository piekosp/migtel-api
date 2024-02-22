from rest_framework.permissions import BasePermission

from .models import User


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in User.MANAGER_ROLES


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ANALYST


class IsManagerOrSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role in User.MANAGER_ROLES or obj == request.user


class CanDeleteUser(BasePermission):
    def has_permission(self, request, view):
        if request.method != "DELETE":
            return True
        return request.user.role == User.ADMIN


class CanSeeUserDetails(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.role not in User.EMPLOYEE_ROLES:
            return request.user.role == User.ADMIN or request.user == obj
        return True


class CanEditUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role not in User.MANAGER_ROLES:
            return request.user == obj
        if request.user.role == User.MANAGER:
            return obj.role in User.EMPLOYEE_ROLES
        return True


class CanEditUserRole(BasePermission):
    def has_permission(self, request, view):
        role = request.data.get("role")
        if not role:
            return True
        if request.user.role == User.ADMIN:
            return True
        return role in User.EMPLOYEE_ROLES

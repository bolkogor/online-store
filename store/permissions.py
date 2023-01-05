from rest_framework import permissions


class ReadOnlyOrSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.method in permissions.SAFE_METHODS


class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user == obj.user
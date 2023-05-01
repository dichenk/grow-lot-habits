from rest_framework.permissions import BasePermission


class Owner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class IsUptTIK(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'upttik')


class IsStaffProdi(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'staffprodi')

class IsMahasiswa(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'mahasiswa')
    

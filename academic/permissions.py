from rest_framework.permissions import BasePermission


upt_tik = 'upttik'
staff_prodi = 'staffprodi'
mahasiswa = 'mahasiswa'


class IsUptTIK(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, upt_tik)


class IsStaffProdi(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, staff_prodi)


class IsMahasiswa(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, mahasiswa)
    

class IsUptTIkOrIsStaffProdi(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, upt_tik) or hasattr(request.user, staff_prodi)
    

class IsStaffProdiOrIsMahasiswa(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, staff_prodi) or hasattr(request.user, mahasiswa)
    

class IsUptTIKOrIsMahasiswa(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, upt_tik) or hasattr(request.user, mahasiswa)


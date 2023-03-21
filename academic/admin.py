from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import models


@admin.register(models.UptTIK)
class UptTIKAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']

    def isUptTIKUser(self, request):
        return hasattr(request.user, 'upttik')
    
    def get_queryset(self, request):
        return models.UptTIK.objects.filter(user_id=request.user.id)
    
    def has_add_permission(self, request):
        if self.isUptTIKUser(request):
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=models.UptTIK):
        if self.isUptTIKUser(request):
            return False
        return super().has_delete_permission(request, obj)
    
    def changelist_view(self, request, extra_context=None):
        if self.isUptTIKUser(request):
            upttik = self.get_queryset(request).first()
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[upttik.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
    

@admin.register(models.Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama']
    ordering = ['id']


@admin.register(models.Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['no']
    ordering = ['no']


@admin.register(models.ProgramPendidikan)
class ProgramPendidikanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama']


@admin.register(models.GedungKuliah)
class GedungKuliahAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama']
    ordering = ['id']
        

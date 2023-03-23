from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

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


class FilterJurusanInline(admin.TabularInline):
    extra = 0
    model = models.PemberitahuanJurusan
    verbose_name = ''
    verbose_name_plural = 'Filter'


class FilterProdiInline(admin.TabularInline):
    extra = 0
    model = models.PemberitahuanProdi
    verbose_name = ''
    verbose_name_plural = 'Filter'


@admin.register(models.Pemberitahuan)
class PemberitahuanAdmin(admin.ModelAdmin):
    fields = ['judul', 'sub_judul', 'detail', 'tanggal_hapus', 'file', 'link', 'thumbnail', 'preview']
    list_display = ['id', 'judul', 'tanggal_terbit', 'tanggal_hapus']
    list_per_page = 10
    ordering = ['-tanggal_terbit']
    readonly_fields = ['preview']
    search_fields = ['judul']

    def isStaffProdi(self, request):
        return hasattr(request.user, 'staffprodi')

    def preview(self, pemberitahuan):
        if pemberitahuan.thumbnail:
            return format_html(f"<img class='thumbnail' src='/media/{pemberitahuan.thumbnail}' />")
        return None
    
    def get_queryset(self, request):
        if self.isStaffProdi(request):
            return models.Pemberitahuan.objects.filter(
                Q(filter_prodi__prodi=request.user.staffprodi.prodi) | Q(filter_prodi__isnull=True)
            )
            
        return super().get_queryset(request)
    
    def get_inline_instances(self, request, obj=None):
        if self.isStaffProdi(request):
            return []
        return [FilterJurusanInline(self.model, self.admin_site), 
                FilterProdiInline(self.model, self.admin_site)]
            
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if self.isStaffProdi(request):
            models.PemberitahuanProdi.objects.create(
                pemberitahuan_id=obj.id,
                prodi=request.user.staffprodi.prodi
            )
            
    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.ProgramStudi)
class ProgramStudiAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'tanggal_sk', 
                    'tahun_operasional', 'jurusan']
    search_fields = ['nama']

    def changelist_view(self, request, extra_context=None):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[prodi.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
    

@admin.register(models.StaffProdi)
class StaffProdiAdmin(admin.ModelAdmin):
    autocomplete_fields = ['prodi', 'user']
    list_display = ['no_induk', 'nama', 'email', 'username']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['user__first_name']

    def nama(self, staff_prodi):
        return f'{staff_prodi.user.first_name} {staff_prodi.user.last_name}'
    
    def changelist_view(self, request, extra_context=None):
        if hasattr(request.user, 'staffprodi'):
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[request.user.staffprodi.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
    

@admin.register(models.Dosen)
class DosenAdmin(admin.ModelAdmin):
    autocomplete_fields = ['prodi']
    list_display = ['nip', 'nama', 'no_hp', 'gelar', 'prodi']
    list_per_page = 10
    readonly_fields = ['preview']
    search_fields = ['nama']

    def preview(self, dosen):
        if dosen.foto_profil:
            return format_html(f'<img class="thumbnail" src="/media/{dosen.foto_profil}" />')
        return None

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            return models.Dosen.objects.filter(prodi=request.user.staffprodi.prodi)
        return super().get_queryset(request)

    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.Kelas)
class KelasAdmin(admin.ModelAdmin):
    autocomplete_fields = ['prodi']
    list_display = ['id', 'prodi', 'semester', 'huruf', 'mahasiswa']
    list_per_page = 10
    ordering = ['semester', 'huruf']
    search_fields = ['prodi']

    def mahasiswa(self, kelas):
        query_str = f'?kelas_id={kelas.id}'
        url = reverse(f'admin:academic_mahasiswa_changelist') + query_str
        return format_html(f'<a class="btn-link" href="{url}">Mahasiswa</a>')
        
    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            return models.Kelas.objects.filter(prodi=request.user.staffprodi.prodi)
        return super().get_queryset(request)

    class Media:
        css = {
            "all": ["academic/styles.css"]
        }


class MahasiswaFilter(admin.SimpleListFilter):
    title = 'semester'
    parameter_name = 'semester'

    def lookups(self, request, model_admin):
         return [(semester.no, f'Semester {semester.no}') for semester in list(models.Semester.objects.all())]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(kelas__semester=self.value())
        return queryset.all()


@admin.register(models.Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    autocomplete_fields = ['pembimbing_akademik', 'user']
    fields = ['nim', 'tanggal_lahir', 'no_hp', 'alamat', 
              'tahun_angkatan', 'pembimbing_akademik', 'kelas',
              'user', 'foto_profil', 'preview']
    list_display = ['nim', 'nama', 'username', 'kelas']
    list_filter = [MahasiswaFilter]
    list_per_page = 10
    search_fields = ['nama']
    readonly_fields = ['preview']

    def preview(self, mahasiswa):
        if mahasiswa.foto_profil:
            return format_html(f'<img class="thumbnail" src="/media/{mahasiswa.foto_profil}" />')
        return None

    def nama(self, mahasiswa):
        return f'{mahasiswa.user.first_name} {mahasiswa.user.last_name}'

    def username(self, mahasiswa):
        return mahasiswa.user.username

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            return models.Mahasiswa.objects.filter(kelas__prodi=prodi)
        return super().get_queryset(request)

    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.Ruangan)
class RuanganAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'gedung', 'aduan']
    list_filter = ['gedung']
    search_fields = ['nama']
    list_per_page = 10

    def aduan(self, ruangan):
        query_str = f"?ruangan_id={ruangan.id}"
        url = reverse('admin:academic_aduanruangan_changelist') + query_str
        return format_html(f'<a class="btn-link" href="{url}">Aduan</a>')

    class Media:
        css = {
            'all': ['academic/styles.css']
        }
    

@admin.register(models.AduanRuangan)
class AduanRuanganAdmin(admin.ModelAdmin):
    list_display = ['id', 'detail', 'ruangan', 'status']
    list_editable = ['status']
    list_per_page = 10
    readonly_fields = ['detail', 'ruangan', 'foto', 'preview']
    search_fields = ['detail']

    def preview(self, aduan_ruangan):
        if aduan_ruangan.foto:
            return format_html(f'<img class="bigger-edthumbnail" src="/media/{aduan_ruangan.foto}" />')
        return None

    class Media:
        css = {
            'all': ['academic/styles.css']
        }


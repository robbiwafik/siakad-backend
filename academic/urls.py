from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register('dosen', views.DosenViewSet, basename='dosen')
router.register('gedung', views.GedungKuliahViewSet, basename='gedung')
router.register('jurusan', views.JurusanViewSet, basename='jurusan')
router.register('karya_ilmiah', views.KaryaIlmiahViewSet, basename='karya_ilmiah')
router.register('kelas', views.KelasViewSet, basename='kelas')
router.register('mahasiswa', views.MahasiswaViewSet, basename='mahasiswa')
router.register('prodi', views.ProgramStudiViewSet, basename='prodi')
router.register('program_pendidikan', views.ProgramPendidikanViewSet, basename='program_pendidikan')
router.register('semester', views.SemesterViewSet, basename='semester')
router.register('staff_prodi', views.StaffProdiViewSet, basename='staff_prodi')

router.register('ruangan', views.RuanganViewSet, basename='ruangan')
ruangan_aduan = routers.NestedSimpleRouter(router, 'ruangan', lookup='ruangan')
ruangan_aduan.register('aduan', views.AduanRuanganViewSet, basename='ruangan-aduan')

router.register('pemberitahuan', views.PemberitahuanViewSet, basename='pemberitahuan')
pemberitahuan_prodi = routers.NestedDefaultRouter(router, 'pemberitahuan', lookup='pemberitahuan')
pemberitahuan_prodi.register('prodi', views.PemberitahuanProdiViewSet, basename='pemberitahuan-prodi')
pemberitahuan_jurusan = routers.NestedDefaultRouter(router, 'pemberitahuan', lookup='pemberitahuan')
pemberitahuan_jurusan.register('jurusan', views.PemberitahuanJurusanViewSet, basename='pemberitahuan-jurusan')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(ruangan_aduan.urls)),
    path('', include(pemberitahuan_prodi.urls)),
    path('', include(pemberitahuan_jurusan.urls))
]

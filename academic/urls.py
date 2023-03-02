from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('jurusan', views.JurusanViewSet, basename='jurusan')
router.register('semester', views.SemesterViewSet, basename='semester')
router.register('program_pendidikan', views.ProgramPendidikanViewSet, basename='program_pendidikan')
router.register('gedung', views.GedungKuliahViewSet, basename='gedung')
router.register('pemberitahuan', views.PemberitahuanViewSet, basename='pemberitahuan')
router.register('prodi', views.ProgramStudiViewSet, basename='prodi')
router.register('staff_prodi', views.StaffProdiViewSet, basename='staff_prodi')
router.register('dosen', views.DosenViewSet, basename='dosen')

urlpatterns = router.urls

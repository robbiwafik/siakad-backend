from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('jurusan', views.JurusanViewSet, basename='jurusan')
router.register('semester', views.SemesterViewSet, basename='semester')

urlpatterns = router.urls

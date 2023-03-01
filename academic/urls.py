from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('jurusan', views.JurusanViewSet, basename='jurusan')

urlpatterns = [
    path('', include(router.urls))
]

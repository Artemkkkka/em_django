from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DogViewSet, BreedViewSet

router = DefaultRouter()
router.register(r'dogs', DogViewSet, basename='dog')
router.register(r'breeds', BreedViewSet, basename='breed')

urlpatterns = [
    path('v1/', include(router.urls)),
]

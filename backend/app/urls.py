from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, MascotaViewSet, CitaViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'mascotas', MascotaViewSet, basename='mascota')
router.register(r'citas', CitaViewSet, basename='cita')


urlpatterns = [
    # Endpoints automáticos para CRUD de clientes, mascotas y citas
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    
    
    
    # Endpoints para JWT login y refresh
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


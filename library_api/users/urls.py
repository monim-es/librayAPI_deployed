from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet, RegisterView
from django.urls import path


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]
urlpatterns += router.urls
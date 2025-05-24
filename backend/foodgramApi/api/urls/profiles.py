from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.profiles import UserActionsViewSet

app_name = 'profiles'

router = DefaultRouter()
router.register(r'profiles', UserActionsViewSet, basename='profile-actions')

urlpatterns = [
    path('', include(router.urls)),
] 
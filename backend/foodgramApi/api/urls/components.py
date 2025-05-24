from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.components import ComponentViewSet

app_name = 'components'

router = DefaultRouter()
router.register(r'components', ComponentViewSet, basename='component')

urlpatterns = [
    path('', include(router.urls)),
] 
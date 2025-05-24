from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.dishes import DishViewSet

app_name = 'dishes'

router = DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('', include(router.urls)),
    path('s/<str:hash>/', DishViewSet.as_view({'get': 'short_link'}), name='short-link'),
] 
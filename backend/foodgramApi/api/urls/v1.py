from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('api.urls.components')),
    path('', include('api.urls.dishes')),
    path('', include('api.urls.profiles')),
] 
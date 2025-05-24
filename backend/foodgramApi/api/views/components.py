from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from components.models import Component
from api.serializers.components import ComponentSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

class ComponentViewSet(ReadOnlyModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny] 
    pagination_class = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        title_param = self.request.query_params.get('title')
        
        if title_param:
            queryset = queryset.filter(title__istartswith=title_param)
        
        return queryset

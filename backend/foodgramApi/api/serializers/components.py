from rest_framework import serializers
from ingredients.models import Component


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["id", "title", "unit"]
        read_only_fields = fields
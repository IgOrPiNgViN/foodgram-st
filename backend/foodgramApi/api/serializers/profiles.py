from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
import base64
from django.core.files.base import ContentFile
from recipes.models import Dish
from ..models import Subscription
from dishes.models import Dish as DishModel
from api.serializers.dishes import ShortDishSerializer


User = get_user_model()


class FoodgramUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(follower=request.user).exists()
        return False


class UserWithDishesSerializer(FoodgramUserSerializer):
    dishes = serializers.SerializerMethodField()
    dishes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'dishes', 'dishes_count'
        )

    def get_dishes(self, obj):
        request = self.context.get('request')
        dishes = DishModel.objects.filter(creator=obj)
        return ShortDishSerializer(
            dishes, many=True, context={'request': request}
        ).data

    def get_dishes_count(self, obj):
        return DishModel.objects.filter(creator=obj).count()


class UserProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_pic',)

    def validate_profile_pic(self, value):
        try:
            if not value.startswith("data:image/"):
                raise serializers.ValidationError("Invalid image format")
            format, imgstr = value.split(";base64,")
            data = base64.b64decode(imgstr)
            if len(data) > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image size should not exceed 5MB")
            return value
        except Exception:
            raise serializers.ValidationError("Invalid image data")

    def update(self, instance, validated_data):
        format, imgstr = validated_data["profile_pic"].split(";base64,")
        ext = format.split("/")[-1]
        filename = f"profile_pic_{instance.id}.{ext}"
        data = ContentFile(base64.b64decode(imgstr), name=filename)
        instance.profile_pic.save(filename, data, save=True)
        return instance
    
from rest_framework import serializers
from django.contrib.auth import get_user_model
from components.serializers import ComponentSerializer
from .models import Dish, DishComponent, FavoriteDish, ShoppingList

User = get_user_model()


class DishComponentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='component.id')
    name = serializers.ReadOnlyField(source='component.title')
    measurement_unit = serializers.ReadOnlyField(source='component.unit')
    color = serializers.ReadOnlyField(source='component.color')

    class Meta:
        model = DishComponent
        fields = ('id', 'name', 'measurement_unit', 'quantity', 'color')


class DishSerializer(serializers.ModelSerializer):
    tags = ComponentSerializer(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredients = DishComponentSerializer(source='dish_components', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = serializers.Base64ImageField()

    class Meta:
        model = Dish
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by_users_relations.filter(id=request.user.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.in_shopping_lists_of_users.filter(id=request.user.id).exists()
        return False


class FavoriteDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteDish
        fields = ('user', 'dish')
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        dish = data['dish']
        if FavoriteDish.objects.filter(user=user, dish=dish).exists():
            raise serializers.ValidationError(
                'Это блюдо уже добавлено в избранное'
            )
        return data


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('user', 'dish')
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user
        dish = data['dish']
        if ShoppingList.objects.filter(user=user, dish=dish).exists():
            raise serializers.ValidationError(
                'Это блюдо уже добавлено в список покупок'
            )
        return data 
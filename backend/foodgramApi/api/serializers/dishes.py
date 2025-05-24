from rest_framework import serializers
from django.contrib.auth import get_user_model
from dishes.models import Dish, DishComponent
from components.models import Component
from api.serializers.components import ComponentSerializer
from api.serializers.profiles import FoodgramUserSerializer
import base64
from django.core.files.base import ContentFile
from django.db import transaction
from ..models import Favorite, ShoppingCart

User = get_user_model()


class DishComponentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='component.id')
    name = serializers.ReadOnlyField(source='component.title')
    measurement_unit = serializers.ReadOnlyField(source='component.unit')
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        model = DishComponent
        fields = ('id', 'name', 'measurement_unit', 'amount')


class DishComponentCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Component.objects.all())
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        model = DishComponent
        fields = ('id', 'amount')


class DishListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='color'
    )
    author = FoodgramUserSerializer(read_only=True)
    ingredients = DishComponentSerializer(
        source='dishcomponent_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_list = serializers.SerializerMethodField()
    image = serializers.Base64ImageField()

    class Meta:
        model = Dish
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_list',
            'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.favorited_by_users_relations.filter(user=user).exists()

    def get_is_in_shopping_list(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.in_shopping_lists_of_users.filter(user=user).exists()


class DishCreateSerializer(serializers.ModelSerializer):
    ingredients = DishComponentCreateSerializer(many=True)
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Component.objects.all(),
        slug_field='color'
    )
    image = serializers.Base64ImageField()
    author = FoodgramUserSerializer(read_only=True)

    class Meta:
        model = Dish
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        dish = Dish.objects.create(**validated_data)
        dish.tags.set(tags_data)

        for ingredient_data in ingredients_data:
            DishComponent.objects.create(
                dish=dish,
                component=ingredient_data['id'],
                quantity=ingredient_data['quantity']
            )

        return dish

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            instance.dishcomponent_set.all().delete()
            for ingredient_data in ingredients_data:
                DishComponent.objects.create(
                    dish=instance,
                    component=ingredient_data['id'],
                    quantity=ingredient_data['quantity']
                )

        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def to_representation(self, instance):
        return DishListSerializer(instance, context=self.context).data


class ShortDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name', 'image', 'cooking_time')

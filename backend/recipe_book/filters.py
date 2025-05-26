from django_filters import rest_framework as filters

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )
    category = filters.NumberFilter(field_name='category__id')
    difficulty = filters.CharFilter(field_name='difficulty')

    class Meta:
        model = Recipe
        fields = [
            "is_favorited",
            "is_in_shopping_cart",
            "author",
            "category",
            "difficulty",
        ]

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorited_by__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_shopping_lists__user=user)
        return queryset

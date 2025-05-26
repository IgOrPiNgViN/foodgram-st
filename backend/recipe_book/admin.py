from django.contrib import admin

from .models import Recipe, RecipeCategory, RecipeIngredient, RecipeFavorite, ShoppingList


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1
    autocomplete_fields = ("ingredient",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'favorites_count', 'created_at')
    search_fields = ('title', 'author__username', 'author__email')
    list_filter = ('author', 'category', 'difficulty', 'is_published')
    inlines = (RecipeIngredientInline,)

    def favorites_count(self, obj):
        return obj.favorited_by.count()
    favorites_count.short_description = 'В избранном'


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount', 'notes')
    search_fields = ('recipe__title', 'ingredient__name')
    list_filter = ('recipe', 'ingredient')


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'added_at')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('user', 'recipe')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'added_at', 'is_purchased')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('user', 'recipe', 'is_purchased')

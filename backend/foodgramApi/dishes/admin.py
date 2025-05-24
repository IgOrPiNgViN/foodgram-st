from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Dish, DishComponent, FavoriteDish, ShoppingList


class DishComponentInline(admin.TabularInline):
    model = DishComponent
    extra = 1
    min_num = 1


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cooking_time", "creator", "favorite_count", "ingredients_display", "image_display")
    search_fields = (
        "name",
        "creator__username",
        "creator__first_name",
        "creator__last_name",
    )
    list_filter = ("creator", "created_at")
    inlines = [DishComponentInline]
    readonly_fields = ("favorite_count",)
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "creator",
                "image",
                "text",
                "cooking_time"
            )
        }),
        ("Статистика", {
            "fields": ("favorite_count",)
        }),
    )

    @admin.display(description="В избранном")
    def favorite_count(self, dish):
        return dish.favorited_by_users_relations.count()

    @admin.display(description="Ингредиенты")
    def ingredients_display(self, dish):
        components = dish.dish_components.all()
        if not components.exists():
            return "Нет ингредиентов"
        
        html_content = "<br>".join(
            f"{item.component.title}: {item.quantity} {item.component.unit}"
            for item in components
        )
        return mark_safe(html_content)

    @admin.display(description="Изображение")
    def image_display(self, dish):
        if dish.image and hasattr(dish.image, 'url'):
            return mark_safe(
                f'<img src="{dish.image.url}" '
                'style="max-width: 70px; max-height: 70px; object-fit: cover;" />'
            )
        return "Нет изображения"


@admin.register(DishComponent)
class DishComponentAdmin(admin.ModelAdmin):
    list_display = ("dish", "component", "quantity")
    search_fields = ("dish__name", "component__title")
    list_filter = ("dish", "component")


@admin.register(FavoriteDish)
class FavoriteDishAdmin(admin.ModelAdmin):
    list_display = ("user", "dish", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "dish__name"
    )
    list_filter = ("user", "dish", "created_at")
    ordering = ("-created_at",)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("user", "dish", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "dish__name"
    )
    list_filter = ("user", "dish", "created_at")
    ordering = ("-created_at",)

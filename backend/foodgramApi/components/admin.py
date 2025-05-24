from django.contrib import admin
from .models import Component


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "color", "dish_count")
    search_fields = ("title", "unit")
    list_filter = ("unit", "color")
    ordering = ("title",)

    @admin.display(description="Количество блюд")
    def dish_count(self, component):
        return component.dishes.count()

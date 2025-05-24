from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MinLengthValidator

from components.models import Component

User = get_user_model()

MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1


class Dish(models.Model):
    """Модель блюда"""
    
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_dishes",
        verbose_name="Автор"
    )
    name = models.CharField(
        "Название",
        max_length=256,
        validators=[MinLengthValidator(1)]
    )
    image = models.ImageField(
        "Изображение",
        upload_to="dishes/images/"
    )
    text = models.TextField(
        "Описание",
        validators=[MinLengthValidator(1)]
    )
    ingredients = models.ManyToManyField(
        Component,
        through="DishComponent",
        related_name="dishes",
        verbose_name="Ингредиенты",
    )
    cooking_time = models.PositiveIntegerField(
        "Время приготовления (в минутах)",
        validators=[MinValueValidator(MIN_COOKING_TIME)]
    )
    created_at = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True
    )
    favorited_by_users_relations = models.ManyToManyField(
        User,
        through="FavoriteDish",
        related_name="favorite_dishes",
        verbose_name="Избранное"
    )
    in_shopping_lists_of_users = models.ManyToManyField(
        User,
        through="ShoppingList",
        related_name="shopping_list_dishes",
        verbose_name="Список покупок"
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class DishComponent(models.Model):
    """Связь блюда и компонента"""
    
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="dish_components",
        verbose_name="Блюдо"
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name="dish_components",
        verbose_name="Компонент"
    )
    quantity = models.PositiveIntegerField(
        "Количество",
        validators=[MinValueValidator(MIN_INGREDIENT_AMOUNT)]
    )

    class Meta:
        verbose_name = "Компонент блюда"
        verbose_name_plural = "Компоненты блюда"
        constraints = [
            models.UniqueConstraint(
                fields=["dish", "component"],
                name="unique_dish_component"
            )
        ]

    def __str__(self):
        return f"{self.component.title} - {self.quantity} {self.component.unit}"


class FavoriteDish(models.Model):
    """Модель избранного блюда"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_dish_relations",
        verbose_name="Пользователь"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="favorite_user_relations",
        verbose_name="Блюдо"
    )
    created_at = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Избранное блюдо"
        verbose_name_plural = "Избранные блюда"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "dish"],
                name="unique_favorite_dish"
            )
        ]

    def __str__(self):
        return f"{self.user} добавил {self.dish} в избранное"


class ShoppingList(models.Model):
    """Модель списка покупок"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_list_relations",
        verbose_name="Пользователь"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="shopping_list_user_relations",
        verbose_name="Блюдо"
    )
    created_at = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "dish"],
                name="unique_shopping_list_dish"
            )
        ]

    def __str__(self):
        return f"{self.user} добавил {self.dish} в список покупок"

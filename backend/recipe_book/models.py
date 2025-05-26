from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class RecipeCategory(models.Model):
    """Модель категории рецепта."""
    name = models.CharField(
        'Название категории',
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        'Описание категории',
        blank=True,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория рецепта'
        verbose_name_plural = 'Категории рецептов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_recipes',
        verbose_name='Автор',
    )
    title = models.CharField(
        'Название',
        max_length=200,
    )
    category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Категория',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
    )
    description = models.TextField(
        'Описание',
    )
    ingredients = models.ManyToManyField(
        'ingredient_list.Ingredient',
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1, 'Минимальное время приготовления - 1 минута'),
        ],
    )
    difficulty = models.CharField(
        'Сложность',
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
    )
    servings = models.PositiveSmallIntegerField(
        'Количество порций',
        default=1,
        validators=[
            MinValueValidator(1, 'Минимальное количество порций - 1'),
        ],
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """Модель связи рецепта и ингредиента."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        'ingredient_list.Ingredient',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(1, 'Минимальное количество - 1'),
        ],
    )
    notes = models.CharField(
        'Примечания',
        max_length=200,
        blank=True,
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount} {self.ingredient.measurement_unit}'


class RecipeFavorite(models.Model):
    """Модель избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт',
    )
    added_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'


class ShoppingList(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_lists',
        verbose_name='Рецепт',
    )
    added_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )
    is_purchased = models.BooleanField(
        'Куплено',
        default=False,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list_item',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'

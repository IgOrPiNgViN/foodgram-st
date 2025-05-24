from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Компонент
class Component(models.Model):
    """Модель компонента блюда"""

    title = models.CharField(
        "Название компонента",
        max_length=128,
        unique=True
    )
    unit = models.CharField(
        "Единица измерения",
        max_length=64
    )
    color = models.CharField(
        "Цвет тега",
        max_length=7,
        default="#E26C2D"
    )

    class Meta:
        verbose_name = "Компонент"
        verbose_name_plural = "Компоненты"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}, {self.unit}"

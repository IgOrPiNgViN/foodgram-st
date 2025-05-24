from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Пользователь
class User(AbstractUser):
    """Модель пользователя"""
    
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Имя пользователя содержит недопустимые символы"
            )
        ],
    )
    email = models.EmailField(
        "Email",
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        "Имя",
        max_length=150
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150
    )
    profile_pic = models.ImageField(
        "Аватар",
        upload_to="profiles/avatars/",
        blank=True,
        null=True,
        default="profiles/default.jpg"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username


class UserFollow(models.Model):
    """Модель подписки на пользователя"""
    
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Подписчик"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow"
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('following')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f"{self.follower} подписан на {self.following}"

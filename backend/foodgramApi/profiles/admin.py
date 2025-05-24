from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User, UserFollow


class BaseHasRelationFilter(admin.SimpleListFilter):
    LOOKUP_CHOICES = (
        ("yes", _("Да")),
        ("no", _("Нет")),
    )
    relation_field = None  # Должно быть переопределено в подклассах

    def lookups(self, request, model_admin):
        return self.LOOKUP_CHOICES

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(**{f"{self.relation_field}__isnull": False}).distinct()
        if self.value() == "no":
            return queryset.filter(**{f"{self.relation_field}__isnull": True}).distinct()
        return queryset
    

class UserHasDishesFilter(BaseHasRelationFilter):
    title = _("есть блюда")
    parameter_name = "has_dishes"
    relation_field = "created_dishes"


class UserHasFollowingFilter(BaseHasRelationFilter):
    title = _("есть подписки")
    parameter_name = "has_following"
    relation_field = "following"


class UserHasFollowersFilter(BaseHasRelationFilter):
    title = _("есть подписчики")
    parameter_name = "has_followers"
    relation_field = "followers"


@admin.register(User)
class ExtendedUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "get_full_name",
        "email",
        "get_profile_pic_preview",
        "get_dishes_count",
        "get_following_count",
        "get_followers_count",
        "is_staff",
        "is_active",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    list_filter = (
        "is_staff",
        "is_active",
        UserHasDishesFilter,
        UserHasFollowingFilter,
        UserHasFollowersFilter,
    )
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Личная информация", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "profile_pic"
            )
        }),
        ("Права доступа", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser"
            )
        }),
        ("Важные даты", {
            "fields": (
                "last_login",
                "date_joined"
            )
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    @admin.display(description="ФИО")
    def get_full_name(self, user):
        return f"{user.first_name} {user.last_name}"

    @admin.display(description="Аватар")
    def get_profile_pic_preview(self, user):
        if user.profile_pic:
            return mark_safe(
                f'<img src="{user.profile_pic.url}" '
                'style="max-width: 50px; max-height: 50px; object-fit: cover;" />'
            )
        return "Нет аватара"

    @admin.display(description="Блюд")
    def get_dishes_count(self, user):
        return user.created_dishes.count()

    @admin.display(description="Подписок")
    def get_following_count(self, user):
        return user.following.count()

    @admin.display(description="Подписчиков")
    def get_followers_count(self, user):
        return user.followers.count()


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    search_fields = (
        "follower__username",
        "follower__email",
        "following__username",
        "following__email"
    )
    list_filter = ("follower", "following")
    ordering = ("-created_at",)

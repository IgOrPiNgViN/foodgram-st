import os
from pathlib import Path
import django
from django.core.files import File
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from django.contrib.auth.hashers import make_password  # noqa: E402
from ingredient_list.models import Ingredient  # noqa: E402
from recipe_book.models import Recipe, RecipeIngredient  # noqa: E402
from user_management.models import User  # noqa: E402

def create_test_data():
    print("Creating test data...")
    user1, created1 = User.objects.get_or_create(
        email="user1@example.com",
        defaults={
            "username": "admin_user",
            "first_name": "Admin",
            "last_name": "User",
            "password": make_password("password123"),
            "is_staff": True,
            "is_superuser": True,
        },
    )
    if created1:
        avatar_path = Path("data/demo_avatar_1.png")
        with open(avatar_path, "rb") as f:
            user1.avatar.save("demo_avatar_1.jpg", File(f), save=True)
        print(f"Created administrator user: {user1.email}")
    else:
        print(f"User {user1.email} already exists")
    user2, created2 = User.objects.get_or_create(
        email="user2@example.com",
        defaults={
            "username": "regular_user",
            "first_name": "Regular",
            "last_name": "User",
            "password": make_password("password123"),
            "is_staff": False,
            "is_superuser": False,
        },
    )
    if created2:
        avatar_path = Path("data/demo_avatar_2.png")
        with open(avatar_path, "rb") as f:
            user2.avatar.save("demo_avatar_2.png", File(f), save=True)
        print(f"Created regular user: {user2.email}")
    else:
        print(f"User {user2.email} already exists")
    user3, created3 = User.objects.get_or_create(
        email="user3@example.com",
        defaults={
            "username": "no_avatar_user",
            "first_name": "No",
            "last_name": "Avatar",
            "password": make_password("password123"),
            "is_staff": False,
            "is_superuser": False,
        },
    )
    if created3:
        print(f"Created regular user without avatar: {user3.email}")
    else:
        print(f"User {user3.email} already exists")
    ingredients = {
        "Молоко": "мл",
        "Сахар": "г",
        "Шоколад": "г",
        "Какао": "г",
        "Корица": "щепотка",
        "Зеленый чай": "г",
        "Лимон": "шт",
        "Вода": "мл",
        "Мед": "ст. л.",
        "Мята": "г",
        "Имбирь": "г",
    }
    for name, unit in ingredients.items():
        Ingredient.objects.get_or_create(name=name, measurement_unit=unit)
    hot_chocolate, created_hc = Recipe.objects.get_or_create(
        name="Горячий шоколад",
        defaults={
            "author": user1,
            "text": "Вкуснейший горячий шоколад с корицей - "
            "идеальный напиток для холодного вечера. "
            "Приготовьте напиток,"
            " который согреет вас в непогоду и поднимет настроение.",
            "cooking_time": 15,
        },
    )
    if created_hc:
        image_path = Path("data/demo_image_hot_chocolate.jpg")
        with open(image_path, "rb") as f:
            hot_chocolate.image.save("hot_chocolate.jpg", File(f), save=True)
        hot_chocolate_ingredients = {
            "Молоко": 200,
            "Шоколад": 50,
            "Какао": 20,
            "Сахар": 15,
            "Корица": 1,
        }
        for ing_name, amount in hot_chocolate_ingredients.items():
            ingredient = Ingredient.objects.get(name=ing_name)
            RecipeIngredient.objects.create(
                recipe=hot_chocolate, ingredient=ingredient, amount=amount
            )
        print(f"Created recipe: {hot_chocolate.name}")
    else:
        print(f"Recipe '{hot_chocolate.name}' already exists")
    green_tea, created_gt = Recipe.objects.get_or_create(
        name="Зеленый чай",
        defaults={
            "author": user2,
            "text": "Освежающий зеленый чай с мятой и медом."
            " Этот чай не только вкусный, но и очень полезный."
            " Богат антиоксидантами и поможет взбодриться.",
            "cooking_time": 5,
        },
    )
    if created_gt:
        image_path = Path("data/demo_image_green_tea.jpg")
        with open(image_path, "rb") as f:
            green_tea.image.save("green_tea.jpg", File(f), save=True)
        green_tea_ingredients = {
            "Зеленый чай": 5,
            "Вода": 250,
            "Мед": 1,
            "Мята": 3,
        }
        for ing_name, amount in green_tea_ingredients.items():
            ingredient = Ingredient.objects.get(name=ing_name)
            RecipeIngredient.objects.create(
                recipe=green_tea, ingredient=ingredient, amount=amount
            )
        print(f"Created recipe: {green_tea.name}")
    else:
        print(f"Recipe '{green_tea.name}' already exists")
    lemonade, created_lm = Recipe.objects.get_or_create(
        name="Лимонад",
        defaults={
            "author": user3,
            "text": "Классический домашний лимонад с имбирем и мятой. "
            "Идеальный напиток для жарких летних дней. "
            "Освежающий, кисло-сладкий и очень вкусный!",
            "cooking_time": 10,
        },
    )
    if created_lm:
        image_path = Path("data/demo_image_lemonade.jpg")
        with open(image_path, "rb") as f:
            lemonade.image.save("lemonade.jpg", File(f), save=True)
        lemonade_ingredients = {
            "Лимон": 2,
            "Вода": 500,
            "Сахар": 50,
            "Мята": 5,
            "Имбирь": 10,
        }
        for ing_name, amount in lemonade_ingredients.items():
            ingredient = Ingredient.objects.get(name=ing_name)
            RecipeIngredient.objects.create(
                recipe=lemonade, ingredient=ingredient, amount=amount
            )
        print(f"Created recipe: {lemonade.name}")
    else:
        print(f"Recipe '{lemonade.name}' already exists")
    print("Test data creation completed!")

if __name__ == "__main__":
    create_test_data()

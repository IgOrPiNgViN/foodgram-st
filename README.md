# Foodgram-st

## Описание проекта

Foodgram - это веб-приложение и API для публикации рецептов и составления списка нужных ингредиентов созданные с использованием Django 5. Авторизованные пользователи могут публиковать рецепты, добавлять понравившиеся рецепты в избранное, подписываться на публикации других авторов и формировать список покупок для выбранных рецептов.

Любые посетители сайта могут изучить каталог рецептов.

## Автор

Комбаров Игорь Антонович, студент МИРЭА, группа ИКБО-02-22
[GitHub](https://github.com/IgOrPiNgViN/foodgram-st)

## Структура проекта

### Основные компоненты

- `backend` - API и веб-интерфейс для администратора
  - `run_dev_server.sh` - Скрипт запуска сервера
  - `container-entry-point.sh` - Скрипт запуска сервера в контейнере (Запускается автоматически, при необходимости)
  - `load_ingredients.py` - Скрипт для загрузки списка ингредиентов в БД (Запускается автоматически)
  - `create_test_data.py` - Скрипт для загрузки демонстрационных данных в БД (Запускается автоматически или вручную в зависимости от конфигурации)
- `frontend` - Интерфейс пользователя
- `gateway / nginx` - Веб-сервер
- `db`(Только контейнер, опционально) - База данных: PostgreSQL

### Дополнительные компоненты

- `infra` - Конфигурация для запуска фронт-энда без других сервисов
- `data` - Подготовленные заранее данные(ссылка для совместимости)
- `docs` - документация
- `postman-collection` - Тесты для API

### Файлы

- `docker-compose.yaml` - Конфигурация docker-compose
- `docker-example.env` - Пример файла с переменными окружения для запуска приложения
- `README.md` - Описание проекта
- `setup.cfg` - Конфигурация линтера

## Технологии

### backend

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL

### frontend

- JS
- React

### другое

- Docker / Podman
- NGINX

## Запуск

⚠️ После запуска приложению может понадобиться 3-7 минут на развёртывание(При первом запуске).

Переменная окружения DEMO_DATA=1 отвечает за загрузку демонстрационных данных. Данные авторизации для тестовых пользователей:

- `test_user@foodgram.local`: password123
- Пользователь `test_admin@foodgram.local` - администратор

### Контейнеризированная версия: Быстрый деплой

Скачивания проекта не требуется! Поддерживается только Linux!

Зависимости:

- docker-compose/podman-compose
- wget
- curl
- bash

Docker-compose:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/IgOrPiNgViN/foodgram-st/main/fast_deploy.sh)
```

Podman-compose:

```bash
USE_PODMAN=1 bash <(curl -fsSL https://raw.githubusercontent.com/IgOrPiNgViN/foodgram-st/main/fast_deploy.sh)
```

Что делает скрипт:

1. Скачивает файлы конфигурации
2. Запускает контейнеры через (docker/podman compose)

### Контейнеризированная версия: Со сборкой

```bash
git clone https://github.com/IgOrPiNgViN/foodgram-st.git
cd foodgram-st
cp ./docker-example.env ./docker.env # Create .env file from template
# Edit docker.env file 
docker-compose build 
docker-compose up
```

### Запуск только backend сервера

#### Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

Переменные окружения автоматически загружаются из backend/.env файла. Если он находится в другом каталоге/с другим именем, его потребуется загрузить вручную

Активация .env файла, где ".env" название/путь к файлу:

```bash
set -a
source .env
```

⚠️ Внимание. DEBUG=1 помимо отладочного режима указывает бэкенду, что он должен сам обрабатывать запросы к статике, без nginx.

#### Продакшн

```bash
cd backend
set -a
source .env
python3 -m gunicorn --bind 0.0.0.0:8000 backend.wsgi
```

2ой Вариант:

```bash
cd backend
DEBUG=0 ./run_dev_server.sh
```

#### Сервер разработки

```bash
cd backend
DEBUG=1 ./run_dev_server.sh
```

## Тесты

⚠️ Тесты не совместимы с подготовленными данными(Кроме ингредиентов).

### Линтер

```bash
ruff check backend/
flake8 | grep W
flake8 | grep E
```

### Postman

Смотрите документацию в каталоге postman_collection

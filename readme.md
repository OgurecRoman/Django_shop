Перед началом работы откройте файл example.env, поменяйте значения переменных
при необходимости и сохраните этот файл под названием ".env"

## Активация виртуального окружения
```
python -m venv venv

source venv/bin/activate # для linux

venv/Scripts/activate # для windows
```

## Установка необходимых пакетов
```
python3 -m pip install --upgrade pip

pip install -r requirements/prod.txt # основные зависимости

pip install -r requirements/dev.txt # зависимости для разработки

pip install -r requirements/test.txt # зависимости для тестов
```
## Бейджик
[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/159819-treninasonya-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/159819-treninasonya-course-1112/-/commits/main)

## Запуск сервера
```
python manage.py runserver
```
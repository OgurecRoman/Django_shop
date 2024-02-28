Перед началом работы откройте файл example.env, поменяйте значения переменных
при необходимости и сохраните этот файл под названием ".env"

Структура базы данных представлена в файле ER.jpg

## Активация виртуального окружения
```bash 
python3 -m venv venv

source venv/bin/activate # для linux

venv/Scripts/activate.bat # для windows
```

## Установка необходимых пакетов
```bash
python3 -m pip install --upgrade pip

pip3 install -r requirements/prod.txt # основные зависимости

pip3 install -r requirements/dev.txt # зависимости для разработки

pip3 install -r requirements/test.txt # зависимости для тестов
```

## Бейджик
[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/159819-treninasonya-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/159819-treninasonya-course-1112/-/commits/main)

## Запуск сервера
```bash
python3 manage.py runserver
```
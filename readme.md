.env содержит секретные данные

python -m venv venv

source venv/bin/activate # для linux

venv/Scripts/activate # для windows

python3 -m pip install --upgrade pip

pip install -r requirements/prod.txt # основные зависимости

pip install -r requirements/dev.txt # зависимости для разработки

pip install -r requirements/test.txt # зависимости для тестов

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/159819-treninasonya-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/159819-treninasonya-course-1112/-/commits/main)

python manage.py runserver
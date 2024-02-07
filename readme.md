python -m venv venv

source venv/bin/activate # для linux

venv/Scripts/activate # для windows

python3 -m pip install --upgrade pip

pip install -r requirements/prod.txt # основные зависимости

pip install -r requirements/dev.txt # зависимости для разработки

pip install -r requirements/test.txt # зависимости для тестов

python manage.py runserver
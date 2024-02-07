python -m venv venv

source venv/bin/activate # для linux

venv/Scripts/activate # для windows

python3 -m pip install --upgrade pip

pip install -r requirements.txt

black

black .

python manage.py runserver
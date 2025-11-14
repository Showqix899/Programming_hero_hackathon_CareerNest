#!/bin/bash

echo "🔹 Activating virtual environment..."
source venv/bin/activate

echo "🔹 Installing dependencies..."
pip install -r requirements.txt

echo "🔹 Applying migrations..."
python manage.py makemigrations
python manage.py migrate



echo "🔹 Starting Redis server..."
sudo service redis-server start

echo "🔹 Starting Celery worker..."
celery -A config worker -l info &

echo "🔹 Running Django server..."
python manage.py runserver

echo "🔹 Activating virtual environment..."
source venv/bin/activate

echo "🔹 Starting Redis server..."
sudo service redis-server start

echo "🔹 Starting Celery worker..."
celery -A config worker -l info &

echo "🔹 Running Django server..."
python manage.py runserver

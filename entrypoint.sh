#!/bin/sh

until nc -z $DB_HOST $DB_PORT; do
    sleep 1
done

cd src

python manage.py compilemessages

python manage.py migrate

python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv('ADMIN_USERNAME', 'admin')
email = os.getenv('ADMIN_EMAIL', 'admin@admin.com')
password = os.getenv('ADMIN_PASSWORD', 'admin')

exists_by_username = User.objects.filter(username=username).exists()
exists_by_email = User.objects.filter(email=email).exists()

if not (exists_by_username or exists_by_email):
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
else:
    print(f'Superuser with "{username}" or "{email}" already exists')
EOF

gunicorn settings.wsgi:application --bind 0.0.0.0:8000

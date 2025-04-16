#!/bin/sh

until nc -z $DB_HOST $DB_PORT; do
    sleep 1
done

cd src


python manage.py migrate

python manage.py compilemessages

python manage.py collectstatic --noinput


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


if [ "$GEN_MOCK" = "True" ]; then
    python manage.py genmock
fi


find . -type d -name static | while read dir; do
  inotifywait -m -r -e modify,create,delete "$dir" |
  while read path _ file; do
    python manage.py collectstatic --noinput
  done &
done


if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn settings.wsgi:application --bind 0.0.0.0:8000
fi

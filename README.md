# Django project template
Пустой проект на Django, призванный ускорить разработку веб-приложений.
## Dev:
```bash
# git clone repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# run dev db into docker
docker compose -f docker-compose.yml up -d
# create .env file
# ...
# run migrations
python manage.py makemigrations
python manage.py makemigrations users
python manage.py migrate
# run project
python manage.py runserver 8000 
```
### .env file:
#### Ps. Стоит заметить, что имя базы данных, пользователя, пароль пользователя, хост и порт для подключения к базе данных доложны соблюдать с таковыми в из файла конфигурации `docker-compose.yml`
```bash
# .env
DEBUG=1 # debug mode
SECRET_KEY=secret
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
CORS_ALLOWED_ORIGINS=localhost 127.0.0.1
CORS_ORIGIN_ALLOW_ALL=1
DB_ENGINE=django.db.backends.postgresql
DB_DATABASE=project-db
DB_USER=user-db
DB_PASSWORD=password-project-db
DB_HOST=localhost
DB_PORT=5432
```
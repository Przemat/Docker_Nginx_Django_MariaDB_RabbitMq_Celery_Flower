## Django Development With Docker Compose and Machine

Blog post -> https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/

### OS X Instructions

1. Start new machine - `docker-machine create -d virtualbox dev;`
1. Configure your shell to use the new machine environment - `eval $(docker-machine env dev)`
1. Build images - `docker-compose build`
1. Start services - `docker-compose up -d`
1. Create migrations - `docker-compose run web /usr/local/bin/python manage.py migrate`
1. Grab IP - `docker-machine ip dev` - and view in your browser

### SSL configuration

Add files server.crt and server.key to folder nginx/cert

### Envarment Variable

Create .env file

Here is example:

WEB_KEY="YOUR WEB KEY"

DB_PORT=3306
DB_PASSWORD="YOUR DATABASE PASSWORD"
DB_NAME=Django
DB_USER=root
DB_SERVICE="YOUR ADDRESS"

FLOWER_USER=user
FLOWER_PASSWORD=password

RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=password
CELERY_BROKER=amqp://user:password@rabbit:5672
FLOWER_BROKER=amqp://user:password@rabbit:5672

### Troubleshooting

Table 'Django.todo_item' doesn't exist"

1. Start container - `docker-compose start`
2. Make migrations for todo - `docker exec dockerizing-django_web_1 python3 manage.py makemigrations todo`
3. Migrate todo - `docker exec dockerizing-django_web_1 python3 manage.py migrate todo`

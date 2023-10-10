Python 3.11

Django 3.2

Django Rest Framework 3.12.4

Docker

Запуск проекта в Dev-режиме
Установите и активируйте виртуальное окружение
Установите зависимости из файла requirements.txt
pip install -r requirements.txt

В папке с файлом manage.py выполните команду:
python3 manage.py runserver

Запуск проекта в контейнерах
Запуск проекта с помощью docker compose
Создать директорию для проекта

В директории для проекта создать файл .env Файл .env должен содержать следующие переменные:

POSTGRES_USER=<пользователь_БД> POSTGRES_PASSWORD=<пароль_пользователя_БД> POSTGRES_DB=<имя_БД> DB_HOST: 127.0.0.1 DB_PORT: 5432 SECRET_KEY=<django-insecure-сгенерированный_на_https://djecrety.ir/_ключ_для_джанго>

Устанавливить Docker Compose, для этого поочередно выполнить команды

sudo apt update sudo apt install curl curl -fSL https://get.docker.com -o get-docker.sh sudo sh ./get-docker.sh sudo apt-get install docker-compose-plugin

Запустить Docker Compose в режиме демона

sudo docker compose -f docker-compose.production.yml up -d

Обновить git action

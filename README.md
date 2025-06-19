# **em_django**
**Тестовый проект для закрепления знаний использования Django.**

# Оглавление

- Авторы

- Технологический стек

- Установка и запуск проекта

- API эндпоинты

# Авторы
**(контакт-ссылки для связи по email)**

- [Артем Брагин](mailto:bragin15bragin@yandex.ru) - developer    

# Технологический стек

- Python 3.9+

- Django 4.x

- Django REST Framework

- PostgreSQL

- Docker для контейниризации

- Git для управления версиями

# Установка и запуск проекта
**Ниже приведены команды для клонирования,
настройки и запуска проекта.**

*1. Клонирование репозитория и создание виртуального окружения*
```bash
git clone git@github.com:Artemkkkka/em_django.git
cd em_django

python3 -m venv venv
```
*2. Активация окружения и запуск проекта*
```bash
# macOS/Linux:
source venv/bin/activate
# Windows:
. venv/Scripts/activate

docker-compose build

docker-compose run --rm web-app sh -c "python manage.py migrate"

docker-compose run --rm web-app sh -c "python manage.py createsuperuser"

docker-compose up
```
# API эндпоинты
**Полная спецификация доступна после запуска сервера в [документации API](http://127.0.0.1:8000/swagger/)**

# lk-inventory

## Язык реализации
python 3.8

## Описание сервиса
* TODO добавить описание

## Взаимодействие со сторонними сервисами
* TODO добавить описание

## Разработка

### Установка зависимостей
```shell
python3 -m venv venv
source venv/bin/activate
pip install -U pip pipenv
pipenv install --dev
```

### Локальный запуск

```shell
python3 asgi.py
```

### Локальный Swagger

http://localhost:5000/docs

### Запуск внутри докера

```shell
docker-compose up
```

### Запуск тестов

```shell
pip install tox --quiet
tox
```

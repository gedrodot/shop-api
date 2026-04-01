# E-commerce REST API

## Описание проекта
Backend-сервис для интернет-магазина, предоставляющий REST API для управления пользователями, каталогом товаров, корзиной и оформлением заказов. 



## Стек технологий
* **Язык:** Python 3.11+
* **Фреймворк:** Django 4+, Django REST Framework (DRF)
* **База данных:** PostgreSQL 16
* **Аутентификация:** JWT (djangorestframework-simplejwt)
* **Контейнеризация:** Docker, Docker Compose
* **Тестирование:** Pytest, pytest-django
* **Документация API:** drf-spectacular (Swagger UI)

## Архитектурные решения
* Применена логическая декомпозиция (views / services / serializers / models) для масштабируемости и удобства тестирования.
* Изоляция бизнес-логики: контроллеры отвечают только за маршрутизацию и HTTP-ответы. Вся работа с базой данных и расчеты инкапсулированы в `services.py`.
* Транзакции: оформление заказа (списание баланса, списание остатков со склада, очистка корзины) обернуто в `transaction.atomic()`. В случае ошибки на любом этапе происходит откат состояния БД.
* Устранена проблема N+1 запросов за счет использования `select_related` и `prefetch_related` в слоях агрегации данных.

## Инструкция по запуску

1. Склонируйте репозиторий:
```bash
git clone https://github.com/gedrodot/shop-api
cd shop-api
```
2. Запустите сборку и старт контейнеров:
```bash
docker-compose up -d --build
```
3. Примените миграции базы данных:
```bash
docker-compose exec app python manage.py migrate
```
4. Создайте администратора для управления каталогом:
```bash
docker-compose exec app python manage.py createsuperuser
```
## Документация API
После успешного запуска сервиса интерактивная документация (Swagger) доступна по адресу:
```bash
http://127.0.0.1:8000/api/docs/
```
## Тесты
Для запуска тестов выполните команду:
```bash
docker-compose exec app pytest
```

## Проект ticket_manager

### Ппредусмотрен следующий функционал:

Модуль HTTP API на базе [FastAPI](https://fastapi.tiangolo.com) разделён на логические части и содержит следующие маршруты:
- Добавление нового тикета
- Обновление статуса тикета (обновление доступно только сотруднику имеющему доступ)
- Получение списка всех тикетов связанных с сотрудником 
- Регистрация сотрудника
- Вход в систему
- Выход из системы
- Просмотр информации о своём профиле
- Страница с тикетами прикреплённых к сотруднику с возможностью входа в чат с клиентом (доступен [графический интерфейс](http://localhost/pages))
- Страница чата с возможностью передачи файлов



### Технологии:

Python, FastAPI, Docker, Gunicorn, PostgreSQL, sqlalchemy

### Запуск проекта:

- Клонировать репозиторий:
```
git@github.com:krankir/ticket_manager.git
```
- Сборка проекта (все команды выполняются из директории с файлом docker-compose.yml):
```
$ docker-compose build
```
- Запуск проекта:
```
$ docker-compose up
```
- Для остановки контейнеров Docker:
```
docker-compose down -v      # с их удалением
docker-compose stop         # без удаления

- Или остановить сочетанием клавиш:

Ctrl+C                      # windows, linux
command+C                   # Mac
```

- В директории ticket_manager файл example.env переименовать в .env и заполнить своими данными:
```
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASS
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD

LOG_LEVEL

SECRET_KEY
ALGORITHM
```

- Создать и запустить контейнеры Docker, как указано выше.

- Документация будет доступна по адресу: [документация](http://localhost/docs#/)


### Автор backend'а:

Редько Анатолий 2023 г.
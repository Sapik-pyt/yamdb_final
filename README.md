#yamdb_final sprint 16
![example workflow](https://github.com/Sapik-pyt/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# Проект API YaMDb с применением CI/CD

API YaMDb собирает отзывы пользователей на различные произведения такие как
фильмы, книги и музыка. Для приложения настроен Continuous Integration (CI) и
Continuous Deployment (CD).
### Стек технологий использованный в проекте:
- Python 3.7
- Django 2.2.28
- DRF
- JWT

### Запуск проекта в dev-режиме
- Клонировать репозиторий и перейти в него в командной строке.
- Установите и активируйте виртуальное окружение c учетом версии Python 3.9 (выбираем python не ниже 3.9):

```bash
py -3.9 -m venv venv
```

```bash
source venv/Scripts/activate
```

- Затем нужно установить все зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

- Выполняем миграции:

```bash
python manage.py migrate
```

Создаем суперпользователя, после меняем в админ панели роль с user на admin:

```bash
python manage.py createsuperuser
```

Запускаем проект:

```bash
python manage.py runserver
```

### Примеры работы с API для всех пользователей

Подробная документация доступна по эндпоинту /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится. 

```
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```

### Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладает правами администратора (admin)

### Регистрация нового пользователя
Получить код подтверждения на переданный email.
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

Регистрация нового пользователя:

```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}

```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

### Примеры работы с API для авторизованных пользователей

Добавление категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление категории:

```
Права доступа: Администратор.
DELETE /api/v1/categories/{slug}/
```

Добавление жанра:

```
Права доступа: Администратор.
POST /api/v1/genres/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление жанра:

```
Права доступа: Администратор.
DELETE /api/v1/genres/{slug}/
```

Обновление публикации:

```
PUT /api/v1/posts/{id}/
```

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

Добавление произведения:

```
Права доступа: Администратор. 
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

POST /api/v1/titles/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Добавление произведения:

```
Права доступа: Доступно без токена
GET /api/v1/titles/{titles_id}/
```

```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

Частичное обновление информации о произведении:

```
Права доступа: Администратор
PATCH /api/v1/titles/{titles_id}/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Частичное обновление информации о произведении:
```
Права доступа: Администратор
DEL /api/v1/titles/{titles_id}/
```

По TITLES, REVIEWS и COMMENTS аналогично, более подробно по эндпоинту /redoc/

### Работа с пользователями:

Для работы с пользователя есть некоторые ограничения для работы с ними.
Получение списка всех пользователей.

```
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```

Добавление пользователя:

```
Права доступа: Администратор
Поля email и username должны быть уникальными.
POST /api/v1/users/ - Добавление пользователя
```

```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

Получение пользователя по username:

```
Права доступа: Администратор
GET /api/v1/users/{username}/ - Получение пользователя по username
```

Изменение данных пользователя по username:

```
Права доступа: Администратор
PATCH /api/v1/users/{username}/ - Изменение данных пользователя по username
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Удаление пользователя по username:

```
Права доступа: Администратор
DELETE /api/v1/users/{username}/ - Удаление пользователя по username
```

Получение данных своей учетной записи:

```
Права доступа: Любой авторизованный пользователь
GET /api/v1/users/me/ - Получение данных своей учетной записи
```

Изменение данных своей учетной записи:

- Права доступа: Любой авторизованный пользователь
```
PATCH /api/v1/users/me/ # Изменение данных своей учетной записи
```

* Для подключения GitHub Actions в ```api_yamdb```, необходимо создать директорию 
```.github/workflows``` и скопировать в неё файл ```yamdb_workflow.yml``` из
директории проекта.

* Для прохождения тестов, в директории ```infra```, создать файл ```.env``` с
переменными окружения:
```
# settings.py
SECRET_KEY='<secret_key>'      # стандартный ключ, который создается при старте проекта
DEBUG=False                    # опция отладчика True/False
ALLOWED_HOSTS                  # список хостов/доменов, для которых дотсупен текущий проект

ENGINE=django.db.backends.postgresql
DB_NAME                        # имя БД - postgres (по умолчанию)
POSTGRES_USER                  # логин для подключения к БД - postgres (по умолчанию)
POSTGRES_PASSWORD              # пароль для подключения к БД (установите свой)
DB_HOST=db                     # название сервиса (контейнера)
DB_PORT=5432                   # порт для подключения к БД
```

* В директории проекта ```api_yamdb```, запустить ```pytest```:

## Workflow

Для использования Continuous Integration (CI) и Continuous Deployment (CD): в
репозитории GitHub Actions ```Settings/Secrets/Actions``` прописать Secrets -
переменные окружения для доступа к сервисам:

```
SECRET_KEY                     # стандартный ключ, который создается при старте проекта
DEBUG=False                    # опция отладчика True/False
ALLOWED_HOSTS                  # список хостов/доменов, для которых дотсупен текущий проект

ENGINE=django.db.backends.postgresql
DB_NAME                        # имя БД - postgres (по умолчанию)
POSTGRES_USER                  # логин для подключения к БД - postgres (по умолчанию)
POSTGRES_PASSWORD              # пароль для подключения к БД (установите свой)
DB_HOST=db                     # название сервиса (контейнера)
DB_PORT=5432                   # порт для подключения к БД


PORT                           # порт для подключения(ip сервера)
DOCKER_USERNAME                # имя пользователя в DockerHub
DOCKER_PASSWORD                # пароль пользователя в DockerHub
HOST                           # ip_address сервера
USER                           # имя пользователя
SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)

TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
```

При push в ветку main автоматически отрабатывают сценарии:
* *tests* - проверка кода на соответствие стандарту PEP8 и запуск pytest.
Дальнейшие шаги выполняются только если push был в ветку main;
* *build_and_push_to_docker_hub* - сборка и доставка докер-образов на DockerHub
* *deploy* - автоматический деплой проекта на боевой сервер. Выполняется
копирование файлов из DockerHub на сервер;
* *send_message* - отправка уведомления в Telegram.

## Подготовка удалённого сервера
* Войти на удалённый сервер, для этого необходимо знать адрес сервера, имя
пользователя и пароль. Адрес сервера указывается по IP-адресу или по доменному
имени:
```
ssh <username>@<ip_address>
```

* Остановить службу ```nginx```:
```
sudo systemctl stop nginx
```

* Установить Docker и Docker-compose:
```
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io
sudo apt install docker-compose -y
```

* Проверить корректность установки Docker-compose:
```
sudo docker-compose --version
```
* На сервере создать директорию ```nginx/``` :
```
mkdir -p nginx/
```

* Скопировать файлы ```docker-compose.yaml``` и
```nginx/default.conf``` из проекта (локально) на сервер в
```home/<username>/docker-compose.yaml``` и
```home/<username>/nginx/default.conf``` соответственно:
  * перейти в директорию с файлом ```docker-compose.yaml``` и выполните:
  ```
  scp docker-compose.yaml <username>@<ip_address>:/home/<username>/docker-compose.yaml
  ```
  * перейти в директорию с файлом ```default.conf``` и выполните:
  ```
  scp default.conf <username>@<ip_address>:/home/<username>/nginx/default.conf
  ```

## После успешного деплоя
* Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```

* Для проверки работоспособности приложения, перейти на страницу:
```
http:/<ip_address>/admin/
```

## Документация для YaMDb доступна по адресу:
```
http:/<ip_address>/redoc/
```

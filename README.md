####Survey
## Документация по API

/ - Открывает главную страницу

* login - Вход в аккаунт

* logout - Выход из аккаунта

* register - Регистрация аккаунта

* add_question/ - запрос на добавление вопроса

* delete_question/<int:quest_id> - запрос на удаление вопроса

* update_question/<int:quest_id> - запрос на изменение вопроса

* delete_opt/<int:opt_id> - запрос на удаление опции вопроса (в рамках обновления вопроса)

* add_opt/<int:quest_id> - запрос на добавление опции вопроса (в рамках обновления вопроса)

* add_survey/ - запрос на добавление опроса  

* add_on_list/<int:surv_id> - запрос на добавление вопроса в опрос (в рамках обновления опроса) 

* delete_survey/<int:surv_id> - удаление опроса 

* del_from_list/<int:surv_id>/<int:quest_id> - запрос на удаление вопроса из опроса (в рамках обновления опроса)

* update_survey/<int:surv_id> - запрос изменение опросa (только, титул и описание)

* start_surv/<int:surv_id> - запрос на начало прохождение опроса 

* add_interv/<int:surv_id> - добавление ответов


## Installation and configuration

1. Клонировать репозиторий: 

$git clone https://github.com/me50/zm412.git

2. Открыть папку survey 

$cd zm412

3. Ввести команду в терминале 

$python3 -m venv venv

4. Активировать  venv:

$source venv/bin/activate 

5. Установить пакеты:

$pip install -r requirements.txt

6. Произвести миграцию базы данных:

$python manage.py migrate

7. Добавить учетку суперпользователя:

$python manage.py createsuperuser 

8. Включить локальный сервер:

$python manage.py runserver

9. Открыть страницу в браузере: 

http://127.0.0.1:8000


#### Docker.hub
zm412/survey

docker run --name django-docker -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 zm412/survey




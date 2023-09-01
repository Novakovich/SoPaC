Консольное приложение «Система Проектов и Договоров». Разработано на Django c подключением PostgreSQL БД.
1. Откройте командную строку или терминал.Перейдите в каталог, в который вы хотите клонировать проект.Выполните команду git clone https://github.com/Novakovich/SoPaC.git
2. Создайте виртуальное окружение.
3. Запустите pip install -r requirements.txt
4. Подключаем PostgreSQL БД:
  - Установите PostgreSQL на вашу локальную машину, если вы еще этого не сделали. Вы можете скачать его с официального сайта PostgreSQL.
  - Создайте базу данных PostgreSQL, используя команду createdb SoDaC_DB или в приложении для pgAdmin.
  - Создайте суперюзера с логином и паролем SoDaC_DB. (Также возможно использовать любое название БД, логина и пароля, но необходимо будет заменить данные в settings.py:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SoDaC_DB',
        'USER': 'SoDaC_DB',
        'PASSWORD': 'SoDaC_DB',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
5. В командной строке примените миграции, запустив команду manage.py makemigrations, а затем manage.py migrate.
6. Запустите файл console_interface для работы с консольным приложением.

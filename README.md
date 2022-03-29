# Парсер Яндекс.Маркет

## Настройка установки

## Django
```bash
$ cd backend
$ pip install -r ./requirements.txt
```
### Откройте settings.py и измените данные на собственные
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'CHANGE_YOUR_DATABASE_NAME',
        'USER': 'CHANGE_USER', 
        'PASSWORD': 'CHANGE_YOUR_PASSWORD'
    }
}
EMAIL_HOST = 'YOUR_EMAIL_HOST'
EMAIL_HOST_USER = 'YOUR_EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_HOST_PASSWORD'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
```
### Для работы парсера yamarket.py нужен установленный браузер Google Chrome и Chromedriver, так же измените настройки на свои:
```bash
options.add_argument(f"user-data-dir=YOUR_PATH_PROFILE_CHROME") # Путь до профиля можно найти введя в адресную строку Chrome - chrome://version/
driver = webdriver.Chrome(executable_path='YOUR_PATH_CHROMEDRIVER', chrome_options=options) # путь до chromedriver
```
## ❗❗❗Ремарка по поводу профиля Chrome ❗❗❗
Прежде чем запустить парсер необходимо залогиниться в Яндексе, это необходимо для того, чтобы обходить капчу. Если не хотите использовать дефолтный профиль Chrome, то необходимо указать путь до профиля, в котором так же необходимо пройти авторизацию в Яндексе.

### Запуск Django
```bash
$ python manage.py migrate
$ python manage.py runserver
```

## Запуск Vue
```bash
$ cd frontend
$ npm install
$ npm run serve
```
##Docker
###В корне проекта создать .env.dev и прописать свои настройки
```bash
# Data Base
POSTGRES_DB=имя_твоей_бд
POSTGRES_ENGINE=django.db.backends.postgresql
POSTGRES_USER=имя_твоего_пользователя
POSTGRES_PASSWORD=пароль_бд
POSTGRES_HOST=db
POSTGRES_PORT=5432

#Email

EMAIL_HOST_USER=твой_адрес_email
EMAIL_HOST_PASSWORD=пароль_почты
```
## ❗❗❗Ремарка по поводу профиля Chrome ❗❗❗См. выше. Далее запуск контейнера
```bash
$ cd docker
$ docker-compose up --build

```

## СУБД PostgreSQL
Ссылка, как установить для [Windows](https://www.youtube.com/watch?v=yYJ74Sc7nw8)
Ссылка, как установить для [Linux](https://losst.ru/ustanovka-postgresql-ubuntu-16-04)

Связаться со мной в [Telegram](https://t.me/FalseHuman)

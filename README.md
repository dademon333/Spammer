# Spammer

---

### Микросервис отправки уведомлений и сообщений клиентам одного приложения для записи к бьюти-мастерам

Поддерживается отправка на:
1. Whatsapp
2. Email
3. Sms-сообщения
4. Мобильные уведомления

## Deploy
1. В корне проекта (рядом с docker-compose.yaml) создаем файл .env и заполняем его следующими значениями:
* `POSTGRESQL_USER` - Имя пользователя в базе данных
* `POSTGRESQL_HOST` - Хост бд
* `POSTGRESQL_PORT` - Порт бд
* `POSTGRESQL_PASSWORD` - Пароль от пользователя
* `POSTGRESQL_DATABASE` - Название базы данных

* `SMSC_LOGIN` - Логин от аккаунта smsc  (сторонний сервис для отправки sms-сообщений)
* `SMSC_PASSWORD` - Пароль от аккаунта smsc

* `WAPICO_ACCESS_TOKEN` - access_token от wapico (сторонний сервис для отправки whatsapp-сообщений)

* `EMAIL_ADDRESS` - email компании, с которого будут отправляться сообщения
* `EMAIL_PASSWORD` - Пароль от почтового ящика
* `EMAIL_SERVER_URL` - SMTP-сервер почтового провайдера
* `EMAIL_SERVER_PORT` - Порт SMTP-сервера

2. Устанавливаем docker, docker-compose, python (желательно 3.12), с помощью pip качаем alembic
3. Собираем образы и запускаем postgres:
`docker-compose build && docker-compose up -d postgres`
4. Загружаем схему бд из миграций:
`alemgic upgrade head`
5. Запускаем все остальные сервисы:
`docker-compose up -d`

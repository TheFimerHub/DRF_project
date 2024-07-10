# DRF_PROJECT

## Описание проекта

Приложение разработано с использованием Django и предоставляет следующий функционал:

## Установка

Для установки и запуска проекта выполните следующие шаги:

1. Клонируйте репозиторий:
   ``` bash
   git clone https://github.com/ваш-репозиторий/habit_tracker.git
   cd habit_tracker
   ```

2. Создайте `.env` файл в корне проекта и добавьте следующие переменные окружения:
   ``` plaintext
   # Django secret key for cryptographic signing
   DJANGO_SECRET_KEY=your-secret-key

   # Debug mode toggle (True for development, False for production)
   DJANGO_DEBUG=True

   # Allowed host for the Django application
   DJANGO_ALLOWED_HOST=127.0.0.1

   # Database configuration
   DJANGO_DB_NAME=drf_base
   DJANGO_DB_USER=postgres
   DJANGO_DB_PASSWORD=minilam123
   DJANGO_DB_HOST=localhost
   DJANGO_DB_PORT=5432

   # Redis
   REDIS_URL=redis://127.0.0.1:6379

   # Email
   DJANGO_EMAIL_HOST=smtp.yandex.ru
   DJANGO_EMAIL_PORT=465
   DJANGO_EMAIL_USE_TLS=False
   DJANGO_EMAIL_USE_SSL=True
   DJANGO_EMAIL_HOST_USER=sender.sky@yandex.com
   DJANGO_EMAIL_HOST_PASSWORD=your-password

   # Domain name for the application
   DJANGO_DOMAIN=http://127.0.0.1:8099

   # Cache configuration
   DJANGO_CACHE_ENABLED=True
   DJANGO_CACHE_LOCATION=redis://127.0.0.1:6379/1

   # Cors
   CORS_ALLOWED_ORIGINS=https://read-and-write.example.com,https://read-only.example.com
   CSRF_TRUSTED_ORIGINS=https://read-and-write.example.com
   ```

3. Постройте и запустите контейнеры с использованием Docker Compose:
   ``` bash
   docker-compose up --build
   ```

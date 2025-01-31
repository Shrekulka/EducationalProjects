# Django 4.2 Blog Project

## Обзор проекта

Этот проект представляет собой полнофункциональный блог, разработанный с использованием Django 4.2. Он демонстрирует 
передовые практики разработки на Django и включает в себя широкий спектр функций, характерных для современных 
веб-приложений. Проект служит как образовательный ресурс для изучения Django и связанных технологий, а также как основа 
для создания полноценных веб-приложений.

## Основные функции

1. **Система блога:**
   - Создание, редактирование и удаление статей с богатым текстовым редактором (CKEditor 5) для расширенного 
     форматирования контента
   - Категоризация статей с использованием древовидной структуры (MPTT) для удобной навигации
   - Система тегов для улучшения поиска и группировки связанных статей
   - Отображение похожих статей на основе тегов
   
2. **Пользовательская система:**
   - Регистрация с подтверждением по email для защиты от спама
   - Аутентификация (вход/выход) с возможностью входа как по email, так и по логину
   - Профили пользователей с возможностью редактирования и изменения пароля
   - Система восстановления пароля через email
   
3. Комментарии:
   - Древовидная структура комментариев (MPTT) для удобных обсуждений
   - Возможность ответа на комментарии с сохранением иерархии
   - Модерация комментариев
   - Добавление комментариев без перезагрузки страницы с использованием AJAX
   
4. Поиск:
   - Полнотекстовый поиск с использованием встроенных возможностей PostgreSQL для быстрого и эффективного поиска по 
     контенту
   
5. Дополнительные функции:
   - Система лайков/дислайков для оценки контента без перезагрузки страницы (AJAX)
   - Подписка на обновления блога
   - Форма обратной связи для связи с администрацией сайта с использованием CAPTCHA для защиты от спама
   - Карта сайта (sitemap.xml) для улучшения SEO
   - RSS-лента для удобного отслеживания новых публикаций
   - Реализация счетчика просмотров статей
   - Вывод списка популярных статей за последние 7 дней и за день
   
6. Административные функции:
   - Расширенная панель администратора Django
   - Автоматическое резервное копирование базы данных с использованием Celery Beat
   
7. Технические особенности:
   - Асинхронные задачи с использованием Celery для обработки длительных операций (отправка email, создание резервных 
     копий)
   - Кэширование с использованием Redis для улучшения производительности
   - Докеризация проекта для удобного развертывания и масштабирования
   - Настройка Nginx в качестве прокси-сервера для обработки статических файлов и балансировки нагрузки
   - Использование PostgreSQL в качестве основной базы данных
   - Использование Gunicorn в качестве WSGI-сервера для продакшн-окружения
   - Настройка SSL с помощью Certbot для обеспечения HTTPS соединения

## Установка и запуск

### Предварительные требования

- Docker (версия 20.10 или выше)
- Docker Compose (версия 1.29 или выше)
- Git

### Шаги по установке

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Shrekulka/educationalProjects.git
    cd educationalProjects/python/django/backend
    ```

2. Создайте файл .env.dev в директории docker/env/ и заполните его необходимыми переменными окружения.
   Пример содержимого файла:
    ```bash
    SECRET_KEY='your_secret_key'
    DEBUG=1
    ALLOWED_HOSTS='127.0.0.1 localhost'
    CSRF_TRUSTED_ORIGINS='http://127.0.0.1 http://localhost'
    POSTGRES_DB='your_db_name'
    POSTGRES_USER='your_db_user'
    POSTGRES_PASSWORD='your_db_password'
    POSTGRES_HOST='postgres'
    POSTGRES_PORT=5432
    REDIS_LOCATION='redis://redis:6379/1'
    CELERY_BROKER_URL='redis://redis:6379/0'
    CELERY_RESULT_BACKEND='redis://redis:6379/0'
    RECAPTCHA_PUBLIC_KEY='your_public_key'
    RECAPTCHA_PRIVATE_KEY='your_private_key'
    EMAIL_HOST='your_email_host'
    EMAIL_PORT=your_email_port
    EMAIL_USE_TLS=1
    EMAIL_HOST_USER='your_email'
    EMAIL_HOST_PASSWORD='your_email_password'
    ```

3. Измените настройки в файле settings.py для работы с переменными окружения.

4. Соберите Docker-образы:
    ```bash
    docker compose -f docker-compose.dev.yml build
    ```
   
5. Запустите контейнеры:
    ```bash
    docker compose -f docker-compose.dev.yml up
    ```
   
6. После успешного запуска, создайте суперпользователя:
    ```bash
    docker exec -it django sh
    python manage.py createsuperuser
    ```
   
7. Проект будет доступен по адресу `http://localhost` или `http://127.0.0.1`.

## Использование

- Панель администратора доступна по адресу `http://localhost/admin/`
  Используйте созданные учетные данные суперпользователя для входа.
- В панели администратора вы можете создавать статьи, категории и теги, а также управлять пользователями и комментариями.
- На главной странице сайта вы увидите список опубликованных статей.
- Для создания новой статьи, войдите в систему и используйте соответствующую форму.
- Пользователи могут регистрироваться, оставлять комментарии, ставить лайки/дислайки и подписываться на обновления.

## Разработка

Проект использует Docker для создания изолированной среды разработки. Все необходимые сервисы (Django, PostgreSQL, 
Redis, Celery) запускаются в отдельных контейнерах.

**Для внесения изменений в код:**
1. Измените необходимые файлы
2. Если вы добавили новые зависимости, обновите файл requirements.txt.
3. Пересоберите Docker-образы: `docker compose -f docker-compose.dev.yml build`
4. Перезапустите контейнеры: `docker compose -f docker-compose.dev.yml up`

**Для применения миграций базы данных:**
    ```bash
    docker exec -it django sh
    python manage.py makemigrations
    python manage.py migrate
    ```

### Развертывание
**Для развертывания в продакшн-среде:**
- Создайте файл .env.prod с соответствующими настройками.
- Используйте docker-compose.prod.yml для сборки и запуска контейнеров.
- Настройте Nginx как обратный прокси-сервер.
- Настройте SSL-сертификаты для HTTPS соединения.

## Project Structure

```bash
📁 backend                                        # Корневая директория проекта
│
├── 📁 backend/                                   # Основная директория проекта Django
│   │
│   ├── __init__.py                               # Пустой файл, обозначающий директорию как пакет Python
│   │
│   ├── asgi.py                                   # Точка входа для ASGI-совместимых веб-серверов для запуска проекта
│   │
│   ├── celery.py                                 # Конфигурация Celery для асинхронных задач и фоновых процессов
│   │
│   ├── settings.py                               # Основной файл настроек проекта Django 
│   │
│   ├── urls.py                                   # Главный файл URL-маршрутизации, определяющий пути для всего проекта
│   │   
│   └── wsgi.py                                   # Точка входа для WSGI-совместимых веб-серверов для запуска проекта
│   
├── 📁 cache/                                     # Директория для хранения файлов кэша
│   │ 
│   └── 2ee1e42baa1c3f47432251297a32790b.djcache  # Файла кэша Django
│ 
├── 📁 docker/                                    # Директория с конфигурациями Docker для контейнеризации проекта
│   │
│   ├── 📁 env/                                   # Директория для файлов с переменными окружения
│   │   │
│   │   ├── .env.dev                              # Файл с переменными окружения для среды разработки
│   │   │   
│   │   └── .env.prod                             # Файл с переменными окружения для продакшен-среды
│   │
│   ├── 📁 logs/                                  # Директория для хранения логов Docker-контейнеров
│   │   │
│   │   └── ...                                   # Различные файлы логов
│   │   
│   ├── 📁 nginx/                                 # Директория с конфигурациями Nginx для проксирования запросов
│   │   │
│   │   ├── 📁dev/                                # Nginx для среды разработки
│   │   │   │
│   │   │   └── django.conf                       # Конфигурация Nginx для среды разработки
│   │   │   
│   │   └── 📁prod/                               # Nginx для продакшен-среды
│   │       │
│   │       └── django.conf                       # Конфигурация Nginx для продакшен-среды
│   │ 
│   └── 📁 redis/                                 # Директория с конфигурацией Redis (используется для кэширования 
│       │                                         # и очередей Celery)
│       └── 📁 data/                              # Поддиректория для хранения данных Redis
│           │
│           └── dump.rdb                          # Файл дампа данных Redis
│    
├── 📁 fixtures/                                  # Директория с фикстурами (начальными данными) для базы данных
│   │
│   ├── 📁 blog/                                  # Фикстуры для приложения блога
│   │   │
│   │   ├── article.json                          # Начальные данные для статей блога
│   │   │
│   │   ├── category.json                         # Начальные данные для категорий блога
│   │   │   
│   │   └── comment.json                          # Начальные данные для комментариев
│   │   
│   └── 📁 system/                                # Фикстуры для системного приложения
│       │
│       ├── feedback.json                         # Начальные данные для обратной связи
│       │   
│       └── profile.json                          # Начальные данные для профилей пользователей
│    
├── 📁 media/                                     # Директория для хранения пользовательских медиафайлов
│   │
│   ├── 📁 articles_images/                       # Изображения, относящиеся к статьям блога
│   │   │   
│   │   └── ...                                   # Различные изображения статей
│   │   
│   └── 📁 images/                                # Общая директория для различных типов изображений
│       │
│       ├── 📁 avatars/                           # Изображения аватаров пользователей
│       │   │      
│       │   └── ...                               # Файлы аватаров
│       │
│       └── 📁 thumbnails/                        # Миниатюры изображений
│           │
│           └── ...                               # Файлы миниатюр
│ 
├── 📁 modules/                                   # Директория с модулями (приложениями) проекта
│   │
│   ├── 📁 blog/                                  # Приложение блога
│   │   │
│   │   ├── 📁 migrations/                        # Миграции базы данных для приложения блога
│   │       │
│   │   │   └── ...                               # Файлы миграций
│   │   │
│   │   ├── 📁 templates/                         # HTML-шаблоны для приложения блога
│   │   │   │
│   │   │   └── 📁 blog/                          # Директория приложения блога
│   │   │       │
│   │   │       ├── 📁 articles/                  # Шаблоны для страниц статей
│   │   │       │   │
│   │   │       │   ├── articles_create.html      # Шаблон страницы создания статьи
│   │   │       │   │
│   │   │       │   ├── articles_delete.html      # Шаблон страницы удаления статьи
│   │   │       │   │
│   │   │       │   ├── articles_detail.html      # Шаблон страницы детального просмотра статьи
│   │   │       │   │
│   │   │       │   ├── articles_func_list.html   # Шаблон функционального списка статей
│   │   │       │   │
│   │   │       │   ├── articles_list.html        # Шаблон общего списка статей
│   │   │       │   │
│   │   │       │   └── articles_update.html      # Шаблон страницы обновления статьи
│   │   │       │   
│   │   │       └── 📁 comments/                  # Шаблоны для комментариев
│   │   │           │
│   │   │           └── comments_list.html        # Шаблон списка комментариев
│   │   │
│   │   ├── 📁 templatetags/                      # Пользовательские теги и фильтры шаблонов
│   │   │   │
│   │   │   ├── __init__.py                       # Инициализация пакета тегов
│   │   │   │   
│   │   │   └── blog_tags.py                      # Определения пользовательских тегов для блога
│   │   │
│   │   ├── __init__.py                           # Инициализация приложения блога
│   │   │
│   │   ├── admin.py                              # Настройки админ-панели для моделей блога
│   │   │
│   │   ├── apps.py                               # Конфигурация приложения блога
│   │   │
│   │   ├── feeds.py                              # Настройки RSS-каналов для блога
│   │   │
│   │   ├── forms.py                              # Определения форм для блога (создание/редактирование статей и т.д.)
│   │   │
│   │   ├── models.py                             # Определения моделей данных для блога (статьи, категории, комментарии)
│   │   │
│   │   ├── sitemaps.py                           # Настройки карты сайта для блога
│   │   │
│   │   ├── tests.py                              # Модульные тесты для приложения блога
│   │   │
│   │   ├── urls.py                               # URL-маршруты для приложения блога
│   │   │   
│   │   └── views.py                              # Представления (логика обработки запросов) для блога
│   │ 
│   ├── 📁 services/                              # Общие сервисы и утилиты проекта
│   │   │
│   │   ├── 📁 management/                        # Директория для пользовательских команд управления Django
│   │   │   │   
│   │   │   └── 📁 commands/                      # Пользовательские команды управления Django
│   │   │       │
│   │   │       ├── __init__.py                   # Инициализация пакета команд
│   │   │       │   
│   │   │       └── dbackup.py                    # Команда для создания резервной копии базы данных
│   │   │
│   │   ├── __init__.py                           # Инициализация пакета сервисов
│   │   │
│   │   ├── email.py                              # Функции для работы с электронной почтой
│   │   │
│   │   ├── mixins.py                             # Примеси (mixins) для повторного использования кода
│   │   │
│   │   ├── tasks.py                              # Определения асинхронных задач Celery
│   │   │   
│   │   └── utils.py                              # Общие утилиты и вспомогательные функции
│   │ 
│   ├── 📁 system/                                # Системное приложение (профили пользователей, аутентификация и т.д.)
│   │   │
│   │   ├── 📁 migrations/                        # Миграции базы данных для системного приложения
│   │   │   │
│   │   │   └── ...                               # Файлы миграций
│   │   │
│   │   ├── 📁 templates/                         # HTML-шаблоны для системного приложения
│   │   │   │
│   │   │   └── 📁 system/                        # Поддиректория с именем приложения для предотвращения конфликтов имен
│   │   │       │
│   │   │       ├── 📁 email/                     # Шаблоны электронных писем
│   │   │       │   │
│   │   │       │   ├── activate_email_send.html        # Шаблон письма для активации аккаунта
│   │   │       │   │
│   │   │       │   ├── feedback_email_send.html        # Шаблон письма обратной связи
│   │   │       │   │
│   │   │       │   ├── password_reset_mail.html        # Шаблон письма для сброса пароля
│   │   │       │   │
│   │   │       │   └── password_subject_reset_mail.txt # Тема письма для сброса пароля
│   │   │       │
│   │   │       ├── 📁 errors/                          # Шаблоны страниц ошибок
│   │   │       │   │
│   │   │       │   └── error_page.html                 # Общий шаблон страницы ошибки
│   │   │       │   
│   │   │       ├── 📁 registration/                    # Шаблоны для регистрации и аутентификации
│   │   │       │   │
│   │   │       │   ├── email_confirmation_failed.html  # Шаблон страницы неудачного подтверждения email
│   │   │       │   │
│   │   │       │   ├── email_confirmation_sent.html    # Шаблон страницы отправки подтверждения email
│   │   │       │   │
│   │   │       │   ├── email_confirmed.html            # Шаблон страницы успешного подтверждения email
│   │   │       │   │
│   │   │       │   ├── user_login.html                 # Шаблон страницы входа
│   │   │       │   │
│   │   │       │   ├── user_password_change.html       # Шаблон страницы изменения пароля
│   │   │       │   │
│   │   │       │   ├── user_password_reset.html        # Шаблон страницы сброса пароля
│   │   │       │   │
│   │   │       │   ├── user_password_set_new.html      # Шаблон страницы установки нового пароля
│   │   │       │   │
│   │   │       │   └── user_register.html              # Шаблон страницы регистрации
│   │   │       │   
│   │   │       ├── feedback.html                       # Шаблон страницы обратной связи
│   │   │       │   
│   │   │       ├── profile_detail.html                 # Шаблон страницы детального просмотра профиля
│   │   │       │   
│   │   │       └── profile_edit.html                   # Шаблон страницы редактирования профиля
│   │   │
│   │   ├── __init__.py                                 # Инициализация системного приложения
│   │   │
│   │   ├── admin.py                                    # Настройки админ-панели для системного приложения
│   │   │
│   │   ├── apps.py                                     # Конфигурация системного приложения
│   │   │
│   │   ├── backends.py                                 # Пользовательские бэкенды аутентификации
│   │   │
│   │   ├── forms.py                                    # Определения форм для системного приложения
│   │   │
│   │   ├── middleware.py                               # Пользовательские промежуточные слои (middleware)
│   │   │
│   │   ├── models.py                                   # Определения моделей данных для системного приложения
│   │   │
│   │   ├── tests.py                                    # Модульные тесты для системного приложения
│   │   │
│   │   ├── urls.py                                     # URL-маршруты для системного приложения
│   │   │   
│   │   └── views.py                                    # Представления (логика обработки запросов) для системного 
│   │                                                   # приложения
│   └── __init__.py                                     # Инициализация пакета модулей
│ 
├── 📁 static/                                          # Директория для статических файлов (CSS, JavaScript, изображения)
│   │
│   ├── 📁 css/                                         # CSS файлы
│   │   │
│   │   └── 📁 bootstrap/                               # CSS файлы фреймворка Bootstrap
│   │       │
│   │       └── ...                                     # Различные CSS файлы Bootstrap
│   │
│   ├── 📁 favicon/                                     # Директория для файлов favicon (иконки сайта)
│   │   │
│   │   └── ...                                         # Различные размеры и форматы favicon
│   │
│   ├── 📁 fonts/                                       # Директория для шрифтов
│   │   │
│   │   └── ...                                         # Файлы шрифтов (например, .woff, .ttf)
│   │
│   └── 📁 js/                                          # JS файлы
│       │
│       ├── 📁 bootstrap/                               # JavaScript файлы фреймворка Bootstrap
│       │   │
│       │   └── ...                                     # Различные JS файлы Bootstrap
│       │
│       └── 📁 custom/                                  # Директория для пользовательских JavaScript файлов
│           │
│           ├── backend.js                              # Пользовательский JS для бэкенд-функциональности
│           │
│           ├── comments.js                             # JS для работы с комментариями (например, AJAX-отправка)
│           │
│           ├── profile.js                              # JS для функциональности профиля пользователя
│           │
│           └── ratings.js                              # JS для системы рейтингов (например, лайки/дислайки)
│
├── 📁 staticfiles/                                     # Директория для собранных статических файлов (используется в 
│   │                                                   # продакшене)
│   └── ...                                             # Собранные и оптимизированные статические файлы
│
├── 📁 templates/                                       # Директория для общих шаблонов проекта
│   │
│   ├── 📁 includes/                                    # Директория для включаемых шаблонов (частей страниц)
│   │   │
│   │   ├── latest_comments.html                        # Шаблон для отображения последних комментариев
│   │   │
│   │   └── messages.html                               # Шаблон для отображения системных сообщений (например, ошибок, 
│   │                                                   # уведомлений)
│   ├── header.html                                     # Шаблон для верхней части страницы (header)
│   │
│   ├── main.html                                       # Основной шаблон страницы (базовый макет)
│   │
│   ├── pagination.html                                 # Шаблон для отображения пагинации
│   │
│   └── sidebar.html                                    # Шаблон для боковой панели (sidebar)
│
├── 📁 venv/                                            # Директория виртуального окружения Python
│   │
│   └── ...                                             # Файлы и директории виртуального окружения
│
├── celerybeat-schedule                                 # Файл расписания для Celery Beat (планировщик задач)
│   
├── celerybeat-schedule.db                              # База данных расписания Celery Beat
│   
├── database-2024-06-28-09-07-13.json                   # Файл резервной копии базы данных (дамп в формате JSON)
│   
├── db.json                                             # Текущий дамп данных базы данных в формате JSON
│   
├── db.sqlite3                                          # Файл базы данных SQLite (используется для разработки)
│   
├── docker-compose.dev.yml                              # Конфигурация Docker Compose для среды разработки
│   
├── docker-compose.prod.yml                             # Конфигурация Docker Compose для продакшен-среды
│   
├── Dockerfile                                          # Инструкции для сборки Docker-образа проекта
│   
├── manage.py                                           # Утилита командной строки Django для управления проектом
│   
├── .gitignore                                          # Файл, указывающий Git, какие файлы и директории игнорировать
│   
├── README.md                                           # Файл с описанием проекта, инструкциями по установке и 
│                                                       # использованию
├── requirements.txt                                    # Список зависимостей Python проекта         
│      
├── 📁External Libraries/                               # Директория, отображаемая в IDE (например, PyCharm)
│   │                                                   # Показывает установленные внешние библиотеки Python
│   └── ...                                             # Содержит множество подпапок и файлов внешних библиотек
│   
└── 📁 Scratches and Consoles/                          # Директория, специфичная для IDE (например, PyCharm)
    │                                                   # Используется для временных файлов и консольных сессий
    └── ...                                             # Содержит различные временные файлы и скрипты
```
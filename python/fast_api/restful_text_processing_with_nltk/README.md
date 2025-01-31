# Техническое задание:
##### Описание задачи
Необходимо создать REST API с помощью Python, которое будет взаимодействовать с библиотекой NLTK (Natural Language 
Toolkit). Это API будет использоваться фронтенд-приложением для выполнения разных операций обработки текста.

##### Требования
Использование библиотеки NLTK:
Установите библиотеку NLTK и необходимые пакеты.
Подключить и настроить библиотеки для работы с текстом (например, загрузить нужные наборы данных и модели).

Создание REST API:
Использовать фреймворк для создания API, например Flask или FastAPI.
Создайте несколько эндпоинтов для различных текстовых операций.

Эндпоинты:
1. /tokenize: Токенизация текста.
Метод: POST
Параметры: JSON с полем text.
Ответ: JSON с массивом токенов.
2. /pos_tag: Частоязычная разметка.
Метод: POST
Параметры: JSON с полем text.
Ответ: JSON с массивом пар (токен, тэг).
3. /ner: Распознавание именуемых сущностей.
Метод: POST
Параметры: JSON с полем text.
Ответ: JSON с массивом сущностей и их типов.

##### Требования к коду:
Код должен быть написан на Python 3.
Весь код должен быть хорошо структурирован.
Использовать виртуальную среду для управления зависимостями.
Предоставить README файл с инструкцией по запуску проекта.

# Решение:
Этот проект создает REST API с использованием Python, FastAPI и библиотеки NLTK для обработки текста.

### Вот как он работает:

1. Эндпоинты API:
   - /tokenize: Принимает текст и возвращает список токенов (слов и пунктуации).
   - /pos_tag: Принимает текст и возвращает список кортежей (токен, часть речи).
   - /ner: Принимает текст и возвращает список кортежей (именованная сущность, тип).
   
2. Модели данных:
   Используется Pydantic для валидации входных данных и форматирования ответов API.

3. Логирование:
   Используется стандартный модуль logging для записи сообщений о работе приложения.

### Как работает каждый эндпоинт:
- tokenize: Принимает текст через POST-запрос, асинхронно токенизирует его с помощью функции tokenize_text из service.py 
  и возвращает список токенов.

- pos_tag: Принимает текст через POST-запрос, асинхронно токенизирует его и выполняет частеречную разметку с помощью 
  функции pos_tag_text из service.py, затем возвращает список кортежей (токен, часть речи).

- ner: Принимает текст через POST-запрос, асинхронно токенизирует его, выполняет частеречную разметку и распознает 
  именованные сущности с помощью функции ner_text из service.py, затем возвращает список кортежей (сущность, тип).

### Важные аспекты:
- Асинхронное выполнение: Используется asyncio.to_thread для асинхронного выполнения функций из NLTK, что позволяет 
  избежать блокировки основного потока.

- Логирование ошибок: Обработка и логирование исключений в каждом эндпоинте, чтобы предотвратить падение приложения 
  из-за ошибок.

- Загрузка NLTK ресурсов: Функция download_nltk_resources в utils.py загружает необходимые ресурсы NLTK при запуске 
  приложения для обеспечения корректной работы всех функций NLP.

### Этот проект обеспечивает простой и эффективный способ использования базовых NLP операций через REST API с 
### использованием Python и NLTK, удовлетворяя требованиям технического задания.


## Project Structure

```bash
📁 restful_text_processing_with_nltk/  # Корневая директория проекта
│
├── 📁 src/                            # Исходный код проекта
│   │
│   ├── 📁 nlp/                        # Модуль для обработки естественного языка
│   │   │
│   │   ├── router.py                  # Маршрутизация API и обработка запросов
│   │   │
│   │   ├── schemas.py                 # Схемы данных для валидации запросов и ответов
│   │   │
│   │   ├── service.py                 # Логика обработки текста и вызов моделей NLP
│   │   │
│   │   └── utils.py                   # Вспомогательные функции и утилиты
│   │
│   ├── main.py                        # Основной файл приложения FastAPI
│   │
│   ├── config.py                      # Конфигурационные переменные проекта
│   │   
│   └── logger_config.py               # Конфигурация логирования приложения
│   
│
├── 📁 tests/                           # Тесты для API
│   │ 
│   └── test_api.py                     # Тесты для проверки API эндпоинтов
│ 
├── .gitignore                          # Игнорируемые файлы Git
│   
├── README.md                           # Документация проекта
│      
├── requirements.txt                    # Зависимости проекта
│   
└── 📁 venv/                            # Виртуальная среда Python

```
# Проверка API с использованием Postman и автоматизированных тестов

## Проверка запросов в Postman:

### Откройте Postman и создайте новый запрос для каждого из ваших эндпоинтов.

#### Эндпоинт /tokenize
1. В Postman выберите метод POST.
2. Введите URL: http://localhost:8000/tokenize.
3. В разделе Body выберите raw и формат JSON.
4. В поле ввода JSON вставьте следующий JSON-объект:
    ```bash
    {
        "text": "Hello, world! This is a test."
    }
    ```
5. Нажмите на кнопку "Send" (Отправить).
   Ожидаемый ответ:
   - Статус: 200 OK
   - Тело ответа (во вкладке Pretty):
    ```bash
    {
        "tokens": [
            "Hello",
            ",",
            "world",
            "!",
            "This",
            "is",
            "a",
            "test",
            "."
        ]
    }
    ```
   
#### Эндпоинт /pos_tag
1. В Postman выберите метод POST.
2. Введите URL: http://localhost:8000/pos_tag.
3. В разделе Body выберите raw и формат JSON.
4. В поле ввода JSON вставьте тот же JSON-объект:
    ```bash
    {
        "text": "Hello, world! This is a test."
    }
    ```
5. Нажмите на кнопку "Send" (Отправить).
   Ожидаемый ответ:
   - Статус: 200 OK
   - Тело ответа (во вкладке Pretty):
    ```bash
    {
        "pos_tags": [
            [
                "Hello",
                "NNP"
            ],
            [
                ",",
                ","
            ],
            [
                "world",
                "NN"
            ],
            [
                "!",
                "."
            ],
            [
                "This",
                "DT"
            ],
            [
                "is",
                "VBZ"
            ],
            [
                "a",
                "DT"
            ],
            [
                "test",
                "NN"
            ],
            [
                ".",
                "."
            ]
        ]
    }
    ```

#### Эндпоинт /ner
1. В Postman выберите метод POST.
2. Введите URL: http://localhost:8000/ner.
3. В разделе Body выберите raw и формат JSON.
4. В поле ввода JSON вставьте тот же JSON-объект:
    ```bash
    {
        "text": "Hello, world! This is a test."
    }
    ```
5. Нажмите на кнопку "Send" (Отправить).
   Ожидаемый ответ:
   - Статус: 200 OK
   - Тело ответа (во вкладке Pretty):
    ```bash
    {
        "entities": [
            [
                "Hello",
                "NNP"
            ]
        ]
    }
    ```
   
## Автоматизированное тестирование с использованием Python:

### Файл test_api.py содержит набор тестов для проверки функциональности API. Вот описание каждого теста:

1. test_tokenize()
   - Отправляет POST-запрос на /api/v1/tokenize с текстом "Hello, world!".
   - Проверяет, что код ответа 200 и JSON-ответ содержит ожидаемый список токенов.

2. test_pos_tag()
   - Отправляет POST-запрос на /api/v1/pos_tag с текстом "Hello, world!".
   - Проверяет, что код ответа 200 и JSON-ответ содержит ожидаемый список пар (токен, тег).

3. test_ner()
   - Отправляет POST-запрос на /api/v1/ner с текстом "Hello, John Doe!".
   - Проверяет, что код ответа 200 и в ответе есть хотя бы одна сущность.

4. test_invalid_input()
   - Отправляет POST-запрос на /api/v1/tokenize с пустым текстом.
   - Проверяет, что код ответа 422 (некорректный запрос).

5. test_rate_limit()
   - Отправляет более 10 POST-запросов на /api/v1/tokenize.
   - Проверяет, что последний запрос возвращает код 429 (слишком много запросов).

#### Для запуска автоматизированных тестов используйте команду:
```bash
test_api.py
```
Эти тесты обеспечивают автоматическую проверку основной функциональности API, включая обработку некорректного ввода и 
ограничение частоты запросов.
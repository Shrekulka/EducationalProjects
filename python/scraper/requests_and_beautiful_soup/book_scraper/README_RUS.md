# 1.single_page_scraper.py

## Назначение:
Этот скрипт предназначен для извлечения информации о книгах с одной страницы веб-сайта "https://books.toscrape.com/".

## Структура и работа:
- Импорт необходимых библиотек (requests, BeautifulSoup, logger).
- Определение константы BOOKS_URL с адресом целевой страницы.
- Основная функция main():
    - Отправка GET-запроса на целевую страницу.
    - Парсинг HTML-контента с помощью BeautifulSoup.
    - Поиск и извлечение информации о книгах (изображение, заголовок, цена).
    - Сохранение данных о книгах в список словарей.
    - Логирование процесса и результатов.
- Обработка исключений для устойчивости к ошибкам.

## Особенности:
- Работает только с одной страницей.
- Подробное логирование каждого шага.
- Извлекает базовую информацию о книгах (изображение, заголовок, цена).


# 2. multi_page_scraper.py

## Назначение:
Этот скрипт предназначен для извлечения информации о книгах со всех страниц каталога веб-сайта 
"https://books.toscrape.com/catalogue/".

## Структура и работа:
- Импорт необходимых библиотек.
- Определение констант (BASE_URL, START_URL, USER_AGENT).
- Функции:
    - get_page_content(): получение HTML-контента страницы.
    - parse_books(): извлечение данных о книгах с одной страницы.
    - get_next_page_url(): поиск URL следующей страницы.
    - main(): основная функция, управляющая процессом скрапинга.
- Цикл в main() для обхода всех страниц каталога.
- Обработка исключений для устойчивости к ошибкам.

## Особенности:
- Обрабатывает множество страниц каталога.
- Использует User-Agent для имитации браузера.
- Более структурированный код с разделением на функции.
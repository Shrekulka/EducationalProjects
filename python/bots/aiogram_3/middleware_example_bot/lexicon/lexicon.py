# middleware_example_bot/lexicon/lexicon.py

LEXICON_RU: dict[str, str] = {
    "/start": "Привет{first_name}👋!\n\nЯ эхо-бот для демонстрации работы миддлварей!\n\n"
              "Если хотите - можете мне что-нибудь прислать",
    "no_echo": "Данный тип апдейтов не поддерживается "
               "методом send_copy",
    "button_pressed": "Вы нажали кнопку!"
}

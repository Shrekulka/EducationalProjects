# form_filling_bot_fsm/lexicon/lexicon.py

# Словарь с текстовыми сообщениями для различных сценариев и типов контента на русском языке.
LEXICON_RU: dict[str, str] = {
    "start": "Привет 👋!\n\nУ Вас в настройках чата {language} язык.\n"
             "Этот бот демонстрирует работу FSM\n\n"
             "Чтобы перейти к заполнению анкеты - "
             "отправьте команду /fillform",

    "cancel": "Ей {username} !\n\nОтменять нечего. Вы вне машины состояний\n\n"
              "Чтобы перейти к заполнению анкеты - "
              "отправьте команду /fillform",
    "cancel_out_of_state": "Вы, {full_name}, вышли из машины состояний\n\n"
                           "Чтобы снова перейти к заполнению анкеты - "
                           "отправьте команду /fillform",
    "fillform": "ID №{id} пожалуйста, введите ваше имя",
    "fill_name": "Спасибо {name} !\n\nА теперь введите ваш возраст",
    "warning_invalid_name": "То, что вы отправили не похоже на имя\n\n"
                            "Пожалуйста, введите ваше имя\n\n"
                            "Если вы хотите прервать заполнение анкеты - "
                            "отправьте команду /cancel",
    "fill_age": "Спасибо, Вам {age} лет!\n\nУкажите ваш пол",
    "warning_invalid_age": "Возраст должен быть целым числом от 4 до 120\n\n"
                           "Попробуйте еще раз\n\nЕсли вы хотите прервать "
                           "заполнение анкеты - отправьте команду /cancel",
    "fill_gender": "Спасибо, у тебя пол - {gender}.\n! А теперь загрузите, пожалуйста, ваше фото",
    "warning_invalid_gender": "Пожалуйста, пользуйтесь кнопками "
                              "при выборе пола\n\nЕсли вы хотите прервать "
                              "заполнение анкеты - отправьте команду /cancel",
    "fill_education": "Спасибо!\n\nУкажите ваше образование",
    "warning_invalid_photo": "Пожалуйста, на этом шаге отправьте "
                             "ваше фото\n\nЕсли вы хотите прервать "
                             "заполнение анкеты - отправьте команду /cancel",
    "fill_news": "Спасибо! У тебя образование - {education}.\n\nОстался последний шаг.\n"
                 "Хотели бы вы получать новости?",
    "warning_invalid_news": "Пожалуйста, пользуйтесь кнопками при выборе образования\n\n"
                            "Если вы хотите прервать заполнение анкеты - отправьте "
                            "команду /cancel",
    "fill_wish_news": "Спасибо. Ваш выбор - {wish_news}! Ваши данные сохранены!\n\n"
                      "Вы вышли из машины состояний",
    "view_profile": "Чтобы посмотреть данные вашей "
                    "анкеты - отправьте команду /showdata",
    "warning_invalid_fill_wish_news": "Пожалуйста, воспользуйтесь кнопками!\n\n"
                                      "Если вы хотите прервать заполнение анкеты - "
                                      "отправьте команду /cancel",
    "showdata_available": "Имя: {name}\n"
                          "Возраст: {age}\n"
                          "Пол: {gender}\n"
                          "Образование: {education}\n"
                          "Получать новости: {wish_news}",
    "showdata_unavailable": "Вы еще не заполняли анкету. Чтобы приступить - "
                            "отправьте команду /fillform",
    "echo": "Извините, моя твоя не понимать",
}

# Словарь с текстовыми сообщениями для различных кнопок на русском языке.
LEXICON_BUTTONS: dict[str, str] = {
    "male_button": "Мужской ♂",
    "female_button": "Женский ♀",
    "undefined_button": "🤷 Пока не ясно",
    "secondary_education_button": "Среднее",
    "higher_education_button": "Высшее",
    "without_education_button": "Без образования",
    "yes_news_button": "Да",
    "no_news_button": "Нет, спасибо",
}

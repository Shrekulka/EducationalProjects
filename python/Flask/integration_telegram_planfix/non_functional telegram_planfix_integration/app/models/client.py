# non_functional telegram_planfix_integration/app/models/client.py

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy.orm import relationship

from app import db

print("client.py")


class SessionStatusEnum(Enum):
    """Enum для статусов сессии."""
    ONLINE = "online"
    OFFLINE = "offline"


class Client(db.Model):
    """
    Главный объект, представляющий клиента.

    Модель представляет объект клиента с различными полями для взаимодействия с базой данных и другими интеграциями.
    """
    # 1) Основные поля для таблицы Client

    # уникальный идентификатор клиента в БД
    id: int = db.Column(db.Integer, primary_key=True)

    # Номер телефона
    channel: str = db.Column(db.String(255), nullable=False, unique=True)

    # Токен ПланФикса
    planfix_token: Optional[str] = db.Column(db.String(255), nullable=True)

    # URL ПланФикса
    planfix_url: Optional[str] = db.Column(db.String(255), nullable=True)


    # Связь с сессиями клиента (отношение один ко многим), у клиента может быть несколько сессий
    sessions = db.relationship('Session', back_populates='client')
    # текущая активная сессия
    current_session = db.relationship('Session', uselist=False, backref="client")

    def __init__(self, name, channel, created_at=None, updated_at=None, token=None, user_id=None,
                 name_session=None, path_session=None, chat_id=None, message=None, title=None,
                 contact_id=None, contact_name=None, contact_last_name=None, contact_ico=None,
                 contact_email=None, contact_data=None, attachments_name=None, attachments_url=None,
                 user_email=None, telegram_user_name=None, telegram_user_id=None, token_planfix=None,
                 url_planfix=None, user=None, current_session=None, sessions=None):
        """
                Инициализация клиента с различными параметрами.
        """
        self.name = name
        self.channel = channel
        self.created_at = created_at
        self.updated_at = updated_at
        self.token = token
        self.user_id = user_id
        self.name_session = name_session
        self.path_session = path_session
        self.chat_id = chat_id
        self.message = message
        self.title = title
        self.contact_id = contact_id
        self.contact_name = contact_name
        self.contact_last_name = contact_last_name
        self.contact_ico = contact_ico
        self.contact_email = contact_email
        self.contact_data = contact_data
        self.attachments_name = attachments_name
        self.attachments_url = attachments_url
        self.user_email = user_email
        self.telegram_user_name = telegram_user_name
        self.telegram_user_id = telegram_user_id
        self.token_planfix = token_planfix
        self.url_planfix = url_planfix
        self.user = user
        self.current_session = current_session
        self.sessions = sessions

    # Свойство для сериализации объекта в JSON
    @property
    def serialize(self):
        user_data = self.user.serialize() if self.user else None
        # Формируем словарь для сериализации объекта в JSON
        return {
            'id': self.id,  # Уникальный идентификатор записи
            'name': self.name,  # Название клиента
            'channel': self.channel,  # Номер телефона в міжнародному форматі, без '+'
            'url_planfix': self.url_planfix,  # URL ПланФикса
            'token_planfix': self.token_planfix,  # Токен ПланФикса
            'created_at': self.created_at.isoformat(),  # Время создания записи в формате ISO
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Время последнего обновления записи в формате ISO
            'token': self.token,  # Токен клиента
            'user_id': self.user_id,  # Идентификатор пользователя (внешний ключ)
            'user': user_data,  # Добавлен пользователь в сериализацию
            'name_session': self.name_session,  # Имя сессии
            'path_session': self.path_session,  # Путь к сессии (локальное сховище)
            'chat_id': self.chat_id,  # Уникальный id чата
            'message': self.message,  # Содержимое сообщения
            'title': self.title,  # Заголовок сообщения
            'contact_id': self.contact_id,  # Уникальный идентификатор контакта
            'contact_name': self.contact_name,  # Имя контакта
            'contact_last_name': self.contact_last_name,  # Фамилия контакта
            'contact_ico': self.contact_ico,  # Фото контакта
            'contact_email': self.contact_email,  # Email контакта
            'contact_data': self.contact_data,  # Дополнительные данные контакта
            'attachments_name': self.attachments_name,  # Вложение (имя)
            'attachments_url': self.attachments_url,  # Вложение (ссылка)
            'user_email': self.user_email,  # Email сотрудника-автора исходящего сообщения
            'telegram_user_name': self.telegram_user_name,  # Псевдоним телеграм
            'telegram_user_id': self.telegram_user_id,  # ID юзера телеграм
        }

    @property
    def status(self):
        return SessionStatusEnum.ONLINE.value if self.current_session and self.current_session.is_active \
            else SessionStatusEnum.OFFLINE.value

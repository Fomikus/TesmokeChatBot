from aiogram.filters import Filter, BaseFilter
from typing import Any, Dict, Optional, Union
from aiogram.types import Message, User
import time

import config
import db


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type=None):
        if chat_type is None:
            chat_type = ["group", "supergroup"]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class IsUser(Filter):
    async def __call__(self, message: Message, event_from_user: User):
        return True


class IsModerator(Filter):
    async def __call__(self, message: Message) -> bool:
        db_moder, created = db.User.get_or_create(user_id=message.from_user.id, chat_id=message.chat.id)
        return db_moder.moderator or message.from_user.id in config.ADMINS


class IsMuted(Filter):
    async def __call__(self, message: Message) -> bool:
        db_moder, created = db.User.get_or_create(user_id=message.from_user.id, chat_id=message.chat.id)
        print(db_moder.mute)
        return db_moder.mute > time.time()


class IsDeveloper(Filter):
    async def __call__(self, message: Message, event_from_user: User):
        return event_from_user.id in config.ADMINS


class IsReply(BaseFilter):
    async def __call__(self, message: Message, event_from_user: User):
        return message.reply_to_message is not None


class NewChatMember(BaseFilter):
    async def __call__(self, message: Message, event_from_user: User):
        return message.new_chat_members is not None


class LeftChatMember(BaseFilter):
    async def __call__(self, message: Message, event_from_user: User):
        return message.left_chat_member is not None


class BadWordFilter(BaseFilter):
    async def __call__(self, message: Message, event_from_user: User):
        # fn.contains maybe???
        db_words: list[str] = [x.word for x in db.BadWords.select()]
        for k in db_words:
            if message.text.find(k) != -1:
                return True
        return False



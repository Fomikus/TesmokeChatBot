from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, Update
import db


class AutoRegister(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.chat.type == 'private':
            return await handler(event, data)
        if event.chat.type in ['group', 'supergroup']:
            if event.new_chat_members:
                for k in event.new_chat_members:
                    if not k.is_bot:
                        db_user, created = db.User.get_or_create(user_id=k.id, chat_id=event.chat.id)
                        db_user.save()
            if not event.from_user.is_bot:
                db_user: db.User
                db_user, created = db.User.get_or_create(user_id=event.from_user.id, chat_id=event.chat.id)
                if db_user.username != event.from_user.username:
                    if event.from_user.username is None:
                        db_user.username = 'Нет'
                    else:
                        db_user.username = event.from_user.username.lower()
                    db_user.save()
                return await handler(event, data)

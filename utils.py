import json
import db
import time
from datetime import datetime
from aiogram import Bot
import config


async def log(bot: Bot, text: str):
    chats = []
    if isinstance(config.LOG_CHAT, int) is isinstance(config.LOG_CHAT, str):
        chats.append(int(config.LOG_CHAT))
    else:
        chats = [int(x) for x in config.LOG_CHAT]
    for chat in chats:
        await bot.send_message(chat_id=chat, text=text)


def getUser(name_id: str, chat_id: int):
    if isinstance(name_id, str) and name_id.lower() == 'нет':
        return None
    if isinstance(name_id, int) or name_id.isnumeric():
        db_user: db.User = db.User.get_or_none(db.User.user_id == int(name_id), db.User.chat_id == chat_id)
        if db_user is not None:
            return db_user
    else:
        db_user: db.User = db.User.get_or_none(((db.User.username == name_id.lower()) | (db.User.username == name_id[1:].lower()) | (db.User.username == name_id.lower())), db.User.chat_id == chat_id)
    return db_user

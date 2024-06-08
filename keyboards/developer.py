from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import CallbackData

import db
from CallbackData import *


def dev_menu():
    build = ReplyKeyboardBuilder()
    build.button(text='😡 Плохие слова')
    # build.button(text='🔔 Оповещения')

    return build.as_markup()


def bad_words_menu():
    build = InlineKeyboardBuilder()
    build.button(text='➕ Добавить', callback_data=BadWords(action="add"))
    build.button(text='📋 Список', callback_data=BadWords(action="show"))

    return build.as_markup()


def alerts_menu():
    build = InlineKeyboardBuilder()
    build.button(text='➕ Добавить', callback_data=Alerts(action="add"))
    build.button(text='📋 Список', callback_data=Alerts(action="show"))

    return build.as_markup()


def alerts_list(start=0):
    if isinstance(start, str):
        start = int(start)
    db_alerts: list[str] = [str(x.word) for x in db.Alerts.select()]
    build = InlineKeyboardBuilder()

    if len(db_alerts[start:start+10]) == 0:
        start = max(start-10, 0)

    for word in db_alerts[start:start+10]:
        build.row(
            InlineKeyboardButton(text=word, callback_data=Alerts(action=f"delete", data=word).pack())
        )

    build.row(
        InlineKeyboardButton(text='◀️', callback_data=Alerts(action=f"show", data=str(max(start-10, 0))).pack()),
        InlineKeyboardButton(text=f"{start // 10 + 1}/{(len(db_alerts) // 10) + (1 if len(db_alerts) % 10 != 0 else 0)}", callback_data=Alerts(action=f"nothing").pack()),
        InlineKeyboardButton(text='▶️', callback_data=Alerts(action=f"show", data=str(start+10)).pack())
    )

    return build.as_markup()


def bad_words_list(start=0):
    if isinstance(start, str):
        start = int(start)
    db_bad_words: list[str] = [str(x.word) for x in db.BadWords.select()]
    build = InlineKeyboardBuilder()

    if len(db_bad_words[start:start+10]) == 0:
        start = max(start-10, 0)

    for word in db_bad_words[start:start+10]:
        build.row(
            InlineKeyboardButton(text=word, callback_data=BadWords(action=f"delete", data=word).pack())
        )

    build.row(
        InlineKeyboardButton(text='◀️', callback_data=BadWords(action=f"show", data=str(max(start-10, 0))).pack()),
        InlineKeyboardButton(text=f"{start // 10 + 1}/{(len(db_bad_words) // 10) + (1 if len(db_bad_words) % 10 != 0 else 0)}", callback_data=BadWords(action=f"nothing").pack()),
        InlineKeyboardButton(text='▶️', callback_data=BadWords(action=f"show", data=str(start+10)).pack())
    )

    return build.as_markup()


def bad_words_cancel():
    build = InlineKeyboardBuilder()
    build.button(text='❌ Отмена', callback_data=BadWords(action="cancel"))

    return build.as_markup()


def alerts_cancel():
    build = InlineKeyboardBuilder()
    build.button(text='❌ Отмена', callback_data=Alerts(action="cancel"))

    return build.as_markup()


def example_reply_markup():
    build = ReplyKeyboardBuilder()
    build.button(text='test')
    build.button(text='test')
    build.button(text='test')
    build.button(text='test')
    build.button(text='test')

    build.adjust(2, repeat=True)  # same as
    build.adjust(2, 2, 1)  # this

    return build.as_markup()


def example_reply_markup2():
    build = ReplyKeyboardBuilder()
    build.add(
        KeyboardButton(text='test'),
        KeyboardButton(text='11111')
    )
    build.row(
        KeyboardButton(text='123123321'),
        KeyboardButton(text='123123')
    )
    build.button(text='test')
    # not this is build.adjust(2, 3)

    build.adjust(2, 2, 1)

    return build.as_markup()


def example_inline():
    build = InlineKeyboardBuilder()
    build.button(text='test', callback_data=MyCallback(action="test", id=123))
    build.button(text='test2', callback_data=MyCallback(action="test", id=124))
    return build.as_markup()

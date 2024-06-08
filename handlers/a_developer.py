from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import db
import keyboards as kb
import CallbackData as CbData
import utils
from filters import IsDeveloper, ChatTypeFilter
from states import stBadWords, stAlerts
import utils

dev_route = Router()


@dev_route.message(IsDeveloper(), ChatTypeFilter(), F.text, Command(commands=['addmoder'], prefix="!/", ignore_case=True))
async def addModerCMD(msg: Message, state: FSMContext):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!addmoder @username</code>\nили\n<code>Отправь !addmoder в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    db_target.moderator ^= True
    db_target.save()
    await msg.reply(f"✅ Пользователь [{db_target.username}](tg://user?id={db_target.username}) {'назначен на пост' if db_target.moderator else 'снят с поста'} модератора")
    if db_target.moderator:
        await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) назначил [{db_target.username}](tg://user?id={db_target.username}) на роль модератора")
    else:
        await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) снял [{db_target.username}](tg://user?id={db_target.username}) с поста модератора")


@dev_route.message(IsDeveloper(), ChatTypeFilter(), F.text, Command(commands=['delmoder'], prefix="!/", ignore_case=True))
async def delModerCMD(msg: Message, state: FSMContext):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!addmoder @username</code>\nили\n<code>Отправь !delmoder в ответ на сообщение</code>')

    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if not db_target.moderator:
        return await msg.reply('❌ Пользователь не является модератором')

    db_target.moderator = False
    db_target.save()
    await msg.reply(f"✅ Пользователь снят с поста модератора")
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) снял [{db_target.username}](tg://user?id={db_target.username}) с поста модератора")


# ALERTS_NOT_READY
# @dev_route.message(IsDeveloper(), ChatTypeFilter('private'), F.text == '🔔 Оповещения')
# async def alertBtn(msg: Message, state: FSMContext):
#     await state.clear()
#     await msg.reply('🔔 Настройка оповещений', reply_markup=kb.alerts_menu())


# ALERTS_NOT_READY
# @dev_route.callback_query(IsDeveloper(), CbData.Alerts.filter(F.action == 'show'))
# async def badWordsBtn(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
#     await state.clear()
#     try:
#         await query.message.edit_text('📋 Список оповещений', reply_markup=kb.alerts_list(callback_data.data))
#     except:
#         await query.answer('😡 Дальше ничего нет')


# ALERTS_NOT_READY
# @dev_route.callback_query(IsDeveloper(), CbData.Alerts.filter(F.action == 'add'))
# async def addBadWordsQuery(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
#     await state.clear()
#     await state.set_state(stAlerts.add)
#     await query.message.edit_text('❓ Отправь сообщение для оповещение', reply_markup=kb.alerts_cancel())


# ALERTS_NOT_READY
# @dev_route.message(IsDeveloper(), F.text, ChatTypeFilter('private'), stAlerts.add)
# async def addBadWords(msg: Message, state: FSMContext, bot: Bot):
#     await state.update_data(message_id=msg.message_id, from_chat_id=msg.chat.id)


@dev_route.message(IsDeveloper(), ChatTypeFilter('private'), F.text == '😡 Плохие слова')
async def badWordsBtn(msg: Message, state: FSMContext):
    await state.clear()
    await msg.reply('😡 Плохие слова', reply_markup=kb.bad_words_menu())


@dev_route.callback_query(IsDeveloper(), CbData.BadWords.filter(F.action == 'show'))
async def badWordsBtn(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
    await state.clear()
    try:
        await query.message.edit_text('📋 Список плохих слов', reply_markup=kb.bad_words_list(callback_data.data))
    except:
        await query.answer('😡 Дальше ничего нет')


@dev_route.callback_query(IsDeveloper(), CbData.BadWords.filter(F.action == 'delete'))
async def badWordsBtn(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
    await state.clear()
    db_word: db.BadWords = db.BadWords.get_or_none(db.BadWords.word == callback_data.data)
    if db_word is not None:
        db_word.delete_instance()
        await query.answer(f"✅ Слово '{callback_data.data}' удалено из списка")
        await utils.log(query.bot, f"✅ [{query.from_user.username}](tg://user?id={query.from_user.username}) удалили слово '{callback_data.data}' из списка плохих слов")
    try:
        await query.message.edit_text('📋 Список плохих слов', reply_markup=kb.bad_words_list(0))
    except:
        await query.answer('😡 Дальше ничего нет')


@dev_route.callback_query(IsDeveloper(), CbData.BadWords.filter(F.action == 'add'))
async def addBadWordsQuery(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(stBadWords.add)
    await query.message.edit_text('❓ Отправь плохие слова, каждое слово с новой строки', reply_markup=kb.bad_words_cancel())


@dev_route.callback_query(IsDeveloper(), CbData.BadWords.filter(F.action == 'nothing'))
async def addBadWordsQuery(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
    await query.answer('❓ Тут ничего нет?')


@dev_route.callback_query(IsDeveloper(), CbData.BadWords.filter(F.action == 'cancel'))
async def addBadWordsQuery(query: CallbackQuery, callback_data: CbData.BadWords, bot: Bot, state: FSMContext):
    await state.clear()
    await query.message.edit_text('😡 Плохие слова', reply_markup=kb.bad_words_menu())


@dev_route.message(IsDeveloper(), F.text, ChatTypeFilter('private'), stBadWords.add)
async def addBadWords(msg: Message, state: FSMContext, bot: Bot):
    bad_words = [x.strip().rstrip() for x in msg.text.split("\n")]
    c = 0
    for word in bad_words:
        db_word, created = db.BadWords.get_or_create(word=word)
        db_word.save()
        if created:
            await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) добавил слово '{word}' в список плохих слов")
            c += 1
    await state.clear()
    await msg.answer(f'✅ Добавлено {c} новых плохих слов')

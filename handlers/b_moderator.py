import aiogram.enums
from aiogram import Router, F, Bot, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ChatPermissions

import config
import db
import keyboards as kb
import CallbackData as CbData
import utils
import time
from filters import IsModerator, ChatTypeFilter, IsReply

moder_route = Router()


@moder_route.message(IsModerator(), ChatTypeFilter(), Command(commands=['kick'], prefix='!/', ignore_case=True))
async def kickCmd(msg: Message, state: FSMContext):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!kick @username</code>\nили\n<code>Отправь !kick в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if db_target.user_id == msg.from_user.id:
        return await msg.reply('❌ Нельзя кикнуть самого себя')

    if db_target.user_id in config.ADMINS:
        return await msg.reply('❌ Нельзя кикнуть администратора')

    await msg.bot.ban_chat_member(msg.chat.id, db_target.user_id)
    await msg.bot.unban_chat_member(msg.chat.id, db_target.user_id)
    await msg.reply(f"✅ Пользователь [{db_target.username}](tg://user?id={db_target.username}) кикнут из беседы")
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) кикнул [{db_target.username}](tg://user?id={db_target.username}) из беседы {msg.chat.title} ({msg.chat.id})")


@moder_route.message(IsModerator(), ChatTypeFilter(), Command(commands=['mute'], prefix='!/', ignore_case=True))
async def muteCmd(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!mute @username 10(m/h/d)</code>\nили\n<code>Отправь !mute 10(m/h/d) в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if db_target.user_id == msg.from_user.id:
        return await msg.reply('❌ Нельзя замутить самого себя')

    if db_target.user_id in config.ADMINS:
        return await msg.reply('❌ Нельзя замутить администратора')

    time_char = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60
    }

    if msg.reply_to_message is None and command_args[1][-1] in time_char.keys():
        mute_time = int(command_args[1][:-1]) * time_char[command_args[1][-1]]
    elif command_args[0][-1] in time_char.keys():
        mute_time = int(command_args[0][:-1]) * time_char[command_args[0][-1]]
    else:
        return await msg.reply('❌ Используй\n<code>!mute @username 10(m/h/d)</code>\nили\n<code>Отправь !mute 10(m/h/d) в ответ на сообщение</code>')

    await bot.restrict_chat_member(chat_id=msg.chat.id, user_id=db_target.user_id, permissions=ChatPermissions(
        can_send_messages=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_documents=False,
        can_send_audios=False,
        can_send_polls=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_other_messages=False
    ), until_date=int(time.time() + mute_time))

    await msg.reply(f"✅ Пользователь [{db_target.username}](tg://user?id={db_target.username}) замучен на {mute_time // 60} мин.")
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) замутил [{db_target.username}](tg://user?id={db_target.username}) на {mute_time // 60} минут в беседе {msg.chat.title} ({msg.chat.id})")


@moder_route.message(IsModerator(), ChatTypeFilter(), Command(commands=['unmute'], prefix='!/', ignore_case=True))
async def unmuteCmd(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!unmute @username</code>\nили\n<code>Отправь !unmute в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if db_target.user_id == msg.from_user.id:
        return await msg.reply('❌ Нельзя размутить самого себя')

    await bot.restrict_chat_member(chat_id=msg.chat.id, user_id=db_target.user_id, permissions=ChatPermissions(
        can_send_messages=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_documents=True,
        can_send_audios=True,
        can_send_polls=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_other_messages=True
    ),)

    await msg.reply(f"✅ Пользователь [{db_target.username}](tg://user?id={db_target.username}) размучен")
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) размутил [{db_target.username}](tg://user?id={db_target.username}) в беседе {msg.chat.title} ({msg.chat.id})")


@moder_route.message(IsModerator(), ChatTypeFilter(), Command(commands=['ban'], prefix='!/', ignore_case=True))
async def kickCmd(msg: Message, state: FSMContext):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!ban @username</code>\nили\n<code>Отправь !ban в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if db_target.user_id == msg.from_user.id:
        return await msg.reply('❌ Нельзя забанить самого себя')

    if db_target.user_id in config.ADMINS:
        return await msg.reply('❌ Нельзя забанить администратора')

    await msg.bot.ban_chat_member(msg.chat.id, db_target.user_id)
    await msg.reply(f"✅ Пользователь [{db_target.username}](tg://user?id={db_target.username}) заблокирован")
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) забанил [{db_target.username}](tg://user?id={db_target.username}) в беседе {msg.chat.title} ({msg.chat.id})")


@moder_route.message(IsModerator(), ChatTypeFilter(), Command(commands=['warn'], prefix='!/', ignore_case=True))
async def warnCmd(msg: Message, state: FSMContext):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!ban @username</code>\nили\n<code>Отправь !ban в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if db_target.user_id == msg.from_user.id:
        return await msg.reply('❌ Нельзя заварнить самого себя')

    if db_target.user_id in config.ADMINS:
        return await msg.reply('❌ Нельзя заварнить администратора')

    db_target.warns += 1

    if db_target.warns >= 3:
        await msg.bot.ban_chat_member(chat_id=msg.chat.id, user_id=db_target.user_id)
        await msg.bot.unban_chat_member(chat_id=msg.chat.id, user_id=db_target.user_id)
        await msg.reply(f"Пользователь [{db_target.username}](tg://user?id={db_target.username}) получил 3/3 предупреждений и был кикнут", disable_web_page_preview=True, parse_mode=aiogram.enums.ParseMode.MARKDOWN)
        db_target.warns = 0
    else:
        await msg.reply(f"Пользователь [{db_target.username}](tg://user?id={db_target.username}) получил предупреждение {db_target.warns}/3", disable_web_page_preview=True, parse_mode=aiogram.enums.ParseMode.MARKDOWN)
    db_target.save()
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) заварнил [{db_target.username}](tg://user?id={db_target.username}) в беседе {msg.chat.title} ({msg.chat.id})")


@moder_route.message(IsModerator(), ChatTypeFilter(), Command(commands=['unwarn'], prefix='!/', ignore_case=True))
async def warnCmd(msg: Message, state: FSMContext):
    await state.clear()
    command_args = msg.text.split()[1:]
    if len(command_args) == 0 and msg.reply_to_message is None:
        return await msg.reply('❌ Используй\n<code>!ban @username</code>\nили\n<code>Отправь !ban в ответ на сообщение</code>')
    db_target: db.User = utils.getUser(msg.reply_to_message.from_user.id if msg.reply_to_message else command_args[0], msg.chat.id)

    if db_target is None or (msg.reply_to_message is not None and msg.reply_to_message.from_user.is_bot):
        return await msg.reply('❌ Пользователь не найден')

    if db_target.user_id == msg.from_user.id:
        return await msg.reply('❌ Нельзя заварнить самого себя')

    if db_target.user_id in config.ADMINS:
        return await msg.reply('❌ Нельзя заварнить администратора')

    if db_target.warns > 0:
        db_target.warns -= 1
        await msg.reply(f"С пользователя [{db_target.username}](tg://user?id={db_target.username}) снято предупреждение - {db_target.warns}/3", disable_web_page_preview=True, parse_mode=aiogram.enums.ParseMode.MARKDOWN)
    else:
        await msg.reply(f"У пользователя: [{db_target.username}](tg://user?id={db_target.username}) 0/3 предупреждений", disable_web_page_preview=True, parse_mode=aiogram.enums.ParseMode.MARKDOWN)
    db_target.save()
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) снял варн у [{db_target.username}](tg://user?id={db_target.username}) в беседе {msg.chat.title} ({msg.chat.id})")


@moder_route.message(IsReply(), ChatTypeFilter(), IsModerator(), Command(commands=['del'], prefix='!/', ignore_case=True))
async def delMsg(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    if msg.reply_to_message is not None:
        await msg.reply_to_message.delete()
    await msg.delete()
    await utils.log(msg.bot, f"✅ [{msg.from_user.username}](tg://user?id={msg.from_user.username}) удалил сообщение с текстом \n<code>{msg.reply_to_message.text}</code>\nв беседе {msg.chat.title} ({msg.chat.id})")


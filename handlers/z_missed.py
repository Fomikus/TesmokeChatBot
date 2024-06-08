from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import config
import db
import keyboards as kb
import CallbackData as CbData
import utils
from filters import IsDeveloper, ChatTypeFilter, NewChatMember, LeftChatMember, BadWordFilter

missed_route = Router()


@missed_route.message(ChatTypeFilter(['group', 'supergroup']), Command(commands=['getchat'], prefix="!/", ignore_case=True))
async def delInviteLeaveMsg(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await msg.reply(f"❓ Это беседа - <code>{msg.chat.id}</code>")
    if msg.chat.type == 'group':
        await msg.reply("❗️ Беседа является группой и может превратиться в супер-группу (ID сменится)")


@missed_route.message(NewChatMember())
@missed_route.message(LeftChatMember())
async def delInviteLeaveMsg(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    if msg.new_chat_members is not None:
        for new_member in msg.new_chat_members:
            db_user, created = db.User.get_or_create(user_id=new_member.id, chat_id=msg.chat.id)
            db_user.save()
    await msg.delete()


@missed_route.message(Command(commands=['start', 'help'], prefix='!/', ignore_case=True))
async def helpMsg(msg: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await msg.answer("""Привет!
Для работы у бота должны быть права администратора в беседе

Команды для администраторов:
<code>!ban</code> - бан пользователя и удаление его из чата
<code>!mute 10m</code> (30m, 1h, 6h, 1d) - мут на указанное время (минуты, часы, дни)
<code>!unmute</code> - разрешить отправку сообщений
<code>!warn</code> - варн
<code>!unwarn</code> - снять варн
<code>!kick</code> - кик
<code>!del</code> - удалить сообщение

<code>!addmoder</code> - Добавить модератора
<code>!delmoder</code> - Удалить модератора""", reply_markup=kb.dev_menu() if msg.from_user.id in config.ADMINS else None)


@missed_route.message(BadWordFilter())
async def deleteBadWords(msg: Message, state: FSMContext):
    await state.clear()
    await msg.delete()

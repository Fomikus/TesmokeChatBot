from aiogram.fsm.state import StatesGroup, State


class stBadWords(StatesGroup):
    add = State()


class stAlerts(StatesGroup):
    add = State()
    chat_id = State()
    time = State()
    loop = State()
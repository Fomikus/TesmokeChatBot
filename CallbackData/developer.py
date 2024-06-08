from aiogram.utils.keyboard import CallbackData


class BadWords(CallbackData, prefix='BadWords'):
    action: str
    data: int | str = 0


class Alerts(CallbackData, prefix='Alerts'):
    action: str
    data: int | str = 0

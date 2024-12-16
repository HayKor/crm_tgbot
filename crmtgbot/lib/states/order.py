from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    phone = State()

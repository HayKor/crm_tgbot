from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    shipping = State()
    phone = State()
    fullname = State()

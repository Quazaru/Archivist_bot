from aiogram.fsm.state import StatesGroup, State

class Notes(StatesGroup):
    waiting_for_note = State()

class Collections(StatesGroup):
    waiting_for_name = State()

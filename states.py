from aiogram.fsm.state import StatesGroup, State

class Notes(StatesGroup):
    waiting_for_note = State()
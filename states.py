from aiogram.fsm.state import StatesGroup, State

class Notes(StatesGroup):
    set_text = State()
    get = State()

class Collections(StatesGroup):
    set_name = State()
    get = State()
    

class Menu(StatesGroup):
    is_general = State()
    is_collections = State()
    is_notes = State()

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Меню
menu = [
    [InlineKeyboardButton(text="Добавить заметку", callback_data="add_note")],
    [InlineKeyboardButton(text="Посмотреть заметки", callback_data="view_note_list")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню", callback_data="back_to_menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Выйти в меню", callback_data="back_to_menu")]])


# Добавление заметок
add_note_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сохранить", callback_data="add_note_save")],
    [InlineKeyboardButton(text="Обратно в меню", callback_data="back_to_menu")],
])
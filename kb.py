from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import text
# Меню
menu = [
    [InlineKeyboardButton(text="Добавить коллекцию", callback_data="add_collection")],
    [InlineKeyboardButton(text="Посмотреть коллекции", callback_data="view_collection_list")],
    [InlineKeyboardButton(text="Добавить заметку", callback_data="add_note")],
    [InlineKeyboardButton(text="Посмотреть заметки", callback_data="view_note_list")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню", callback_data="back_to_menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text.back_to_menu, callback_data="back_to_menu")]])


# Добавление заметок
add_note_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сохранить", callback_data="add_note_save")],
    [InlineKeyboardButton(text=text.back_to_menu, callback_data="back_to_menu")],
])

add_note_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сохранить", callback_data="add_note_save")],
        [KeyboardButton(text=text.back_to_menu, callback_data="back_to_menu")],

        ],
     resize_keyboard=True
)
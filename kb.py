from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import text
# Меню
menu = [
    [InlineKeyboardButton(text="Добавить коллекцию", callback_data=text.clbck_collections_set_name)],
    [InlineKeyboardButton(text="Открыть коллекции", callback_data=text.clbck_collections_menu_open)],
    [InlineKeyboardButton(text="Добавить заметку", callback_data=text.clbck_notes_set_text)],
    [InlineKeyboardButton(text="Открыть заметки", callback_data=text.clbck_notes_menu_open)],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню", callback_data=text.clbck_back_to_menu)]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text.menu_goBack, callback_data=text.clbck_back_to_menu)]])


# Просмотр
new_sorting_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=text.extra_arrow_left_outline, callback_data=text.clbck_pages_go_left),
        InlineKeyboardButton(text="По дате создания", callback_data=text.clbck_sort_by_time),
        InlineKeyboardButton(text="По названию", callback_data=text.clbck_sort_by_name),
        InlineKeyboardButton(text=text.extra_arrow_right_outline, callback_data=text.clbck_pages_go_right),
    ],
    [InlineKeyboardButton(text="Назад", callback_data=text.clbck_back_to_menu)]
])
sorting_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="По дате создания", callback_data=text.clbck_sort_by_time),
    InlineKeyboardButton(text="По названию", callback_data=text.clbck_sort_by_name)],
    [InlineKeyboardButton(text="Назад", callback_data=text.clbck_back_to_menu)]
])
# Добавление заметок
add_note_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сохранить", callback_data="add_note_save")],
    [InlineKeyboardButton(text=text.menu_goBack, callback_data=text.clbck_back_to_menu)],
])

add_note_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сохранить", callback_data="add_note_save")],
        [KeyboardButton(text=text.menu_goBack, callback_data=text.clbck_back_to_menu)],

        ],
     resize_keyboard=True
)
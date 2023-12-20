# Спецсимволы (https://getemoji.com/#objects)
extra_arror_right = "⟶"
extra_arror_left = "⟵"
extra_arrow_left_outline = "⇦"
extra_arrow_right_outline = "⇨"


# Меню
menu_greet = "<b> Добро пожаловать в Архив, {user} 😊 </b>"
menu_header = " Коллекция для добавления: {CollectionName} "
menu_goBack = f"{extra_arror_left} Перейти в меню"

# Коллекции 
collection_add_start = "Введите название коллекции:"
collection_add_complete = "Коллекция <b>`{name}`</b> успешно создана!"
collection_menu_header = "<b>💾 Ваши коллекции:</b> \n"
collection_empty = "У вас нет доступных коллекций."

# Заметки
note_add_start = "Отправьте текст, который хотите сохранить:"
note_view_header = "Заметки в <b>`{collection_name}`</b>:"

# СЛУЖЕБНЫЕ
util_still_developing = "Это место всё ещё в разработке 💀💀💀"


## callback_data ##
clbck_collections_set_name = "collections_set_name"
clbck_collections_menu_open = "collections_menu_open"
clbck_notes_set_text = "notes_set_text"
clbck_notes_menu_open = "notes_menu_open"
clbck_sort_by_name = "sort_by_name"
clbck_sort_by_time = "sort_by_time"
clbck_pages_go_left = "pages_go_left"
clbck_pages_go_right = "pages_go_right"
clbck_db_show = "db_show"
clbck_db_open = "db_open"
clbck_db_edit = "db_edit"
clbck_db_delete = "db_edit"

clbck_back_to_menu = "back_to_menu"

## INFO ##
info_database_created = "[INFO] Tables created successfully"
info_database_error = "[ERROR] Error while launching PostgreSQL: {error}"
info_database_closed = "[INFO] PostgreSQL connection closed"
info_notes_error = "Error fetching notes: {error}"
info_colletions_error = "Error fetching collections: {error}"

# LOG
log_any = "[LOG]:{log_name}: {log_value}"

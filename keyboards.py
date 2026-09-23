from telebot import types


# Функция для создания клавиатуры с кнопкой "Купить" (обычная кнопка)
def payment_keyboard(book_key=None):
    keyboard = types.InlineKeyboardMarkup()
    if book_key:
        button = types.InlineKeyboardButton(
            text="💳 Купить книгу за 1 ⭐",
            callback_data=f"buy_{book_key}"
        )
        keyboard.add(button)
    return keyboard


# Функция для создания клавиатуры со списком книг
def books_keyboard(books):
    keyboard = types.InlineKeyboardMarkup()
    for book_key, book in books.items():
        button = types.InlineKeyboardButton(
            text=f"📖 {book['title']}",
            callback_data=f"book_{book_key}"
        )
        keyboard.add(button)
    return keyboard


# Функция для стартовой клавиатуры
def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="📚 Выбрать книгу",
        callback_data="show_books"
    )
    keyboard.add(button)
    return keyboard

from telebot import types


# Кнопка "Купить" для сообщения с описанием (обычная кнопка)
def payment_keyboard(book_key=None):
    keyboard = types.InlineKeyboardMarkup()
    if book_key:
        button = types.InlineKeyboardButton(
            text="💳 Купить за 350 ⭐",
            callback_data=f"buy_{book_key}"
        )
        keyboard.add(button)
    return keyboard


# Кнопка оплаты для СЧЁТА (pay=True) — нужна только внутри send_invoice
def invoice_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Оплатить 350 ⭐",
        pay=True
    )
    keyboard.add(button)
    return keyboard


# Список книг
def books_keyboard(books):
    keyboard = types.InlineKeyboardMarkup()
    for book_key, book in books.items():
        button = types.InlineKeyboardButton(
            text=f"📖 {book['title']}",
            callback_data=f"book_{book_key}"
        )
        keyboard.add(button)
    return keyboard


# Стартовая клавиатура
def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="📚 Выбрать книгу",
        callback_data="show_books"
    )
    keyboard.add(button)
    return keyboard

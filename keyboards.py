from telebot import types


# Функция для создания клавиатуры с кнопкой оплаты
def payment_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Оплатить 1 XTR", pay=True)
    keyboard.add(button)
    return keyboard

# Функция для создания клавиатуры с кнопкой "Купить изображение"
def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Купить изображение", callback_data="buy_image")
    keyboard.add(button)
    return keyboard


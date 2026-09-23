from keyboards import start_keyboard, payment_keyboard, books_keyboard
from db import init_db, save_payment, get_photo_id
from config import TOKEN
import telebot
from telebot import types
import os

bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных
init_db()

# Список книг (можно расширять)
BOOKS = {
    "uzhiny": {
        "title": "Что приготовить на ужин?",
        "description": "50 рецептов для уютных вечеров",
        "file": "KlevakKitchen_Uzhiny.pdf",
        "price": 1,  # цена в XTR (звёздах)
    },
    # Сюда можно добавить следующие книги:
    # "zavtraki": {
    #     "title": "Что приготовить на завтрак?",
    #     "description": "Рецепты для бодрого утра",
    #     "file": "KlevakKitchen_Zavtraki.pdf",
    #     "price": 1,
    # },
}

# ============ ОБРАБОТЧИК КОМАНДЫ /start ============
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в KlevakKitchen! 📚\n\n"
        "Здесь вы можете приобрести мои книги с рецептами.\n\n"
        "Выберите книгу, которую хотели бы приобрести:",
        reply_markup=books_keyboard(BOOKS)
    )

# ============ ОБРАБОТЧИК ВЫБОРА КНИГИ ============
@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def handle_book_choice(call):
    book_key = call.data.replace("book_", "")
    book = BOOKS.get(book_key)
    
    if not book:
        bot.answer_callback_query(call.id, "Книга не найдена")
        return
    
    bot.answer_callback_query(call.id)
    
    # Показываем описание и кнопку покупки
    text = (
        f"📖 *{book['title']}*\n\n"
        f"{book['description']}\n\n"
        f"Цена: {book['price']} ⭐ (Telegram Stars)"
    )
    
    bot.send_message(
        call.message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=payment_keyboard(book_key)
    )

# ============ ОБРАБОТЧИК КНОПКИ "КУПИТЬ" ============
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy(call):
    book_key = call.data.replace("buy_", "")
    book = BOOKS.get(book_key)
    
    if not book:
        bot.answer_callback_query(call.id, "Книга не найдена")
        return
    
    prices = [types.LabeledPrice(label="XTR", amount=book['price'])]
    
    bot.send_invoice(
        call.message.chat.id,
        title=book['title'],
        description=book['description'],
        invoice_payload=f"book_purchase_{book_key}",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=payment_keyboard(book_key)
    )

# ============ ПРОВЕРКА ПЛАТЕЖА ============
@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ============ ОБРАБОТЧИК УСПЕШНОГО ПЛАТЕЖА ============
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    user_id = message.from_user.id
    payment_id = message.successful_payment.provider_payment_charge_id
    amount = message.successful_payment.total_amount
    currency = message.successful_payment.currency
    
    # Определяем, какую книгу купили
    payload = message.successful_payment.invoice_payload
    book_key = payload.replace("book_purchase_", "")
    book = BOOKS.get(book_key)
    
    # Сохраняем информацию о платеже в базу данных
    save_payment(user_id, payment_id, amount, currency)
    
    # Отправляем сообщение о покупке
    bot.send_message(
        message.chat.id,
        "✅ Платеж принят, пожалуйста, ожидайте книгу. Она скоро придёт!"
    )
    
    if not book:
        bot.send_message(message.chat.id, "Извините, книга не найдена.")
        return
    
    # Отправляем PDF-файл
    file_path = book['file']
    if os.path.exists(file_path):
        with open(file_path, 'rb') as document:
            bot.send_document(
                message.chat.id,
                document,
                caption=f"📖 {book['title']}\n\n😊 Спасибо за покупку!"
            )
    else:
        bot.send_message(message.chat.id, "Извините, файл книги не найден.")

# ============ ОБРАБОТЧИК КОМАНДЫ /paysupport ============
@bot.message_handler(commands=['paysupport'])
def handle_pay_support(message):
    bot.send_message(
        message.chat.id,
        "Покупка книги не подразумевает возврат средств.\n"
        "Если у вас есть вопросы, пожалуйста, свяжитесь со мной: @klevakkitchen"
    )

# ============ ЗАПУСК БОТА ============
bot.infinity_polling(interval=0)

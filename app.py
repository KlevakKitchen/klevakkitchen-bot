from flask import Flask
import threading
import os
import bot

app = Flask(__name__)

BOT_STARTED = False


@app.route('/')
def home():
    return "KlevakKitchen bot is running!", 200


def run_bot():
    """Запускаем polling в отдельном потоке"""
    try:
        bot.bot.infinity_polling(interval=0, timeout=20)
    except Exception as e:
        print(f"Bot error: {e}")


if __name__ == "__main__":
    # Запускаем бота только один раз
    if not BOT_STARTED:
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        BOT_STARTED = True

    # Flask-сервер для Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

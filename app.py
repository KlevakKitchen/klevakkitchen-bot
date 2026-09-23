from flask import Flask
import threading
import bot  # запускаем бота в фоне

app = Flask(__name__)


@app.route('/')
def home():
    return "KlevakKitchen bot is running!", 200


def run_bot():
    bot.bot.infinity_polling(interval=0)


if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запускаем Flask-сервер для Render
    app.run(host="0.0.0.0", port=10000)

import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, Dispatcher
from telegram.ext import Updater

# Задайте ваш токен бота
TELEGRAM_BOT_TOKEN = os.environ.get("
8054149603:AAF1Tuuk977Zq7e3jz1dkSfviy5D88rxIEs", "")

app = Flask(__name__)

# Пример данных о компаниях - в реальном приложении данные могут быть из базы
COMPANIES = {
    "1": {"name": "Company A", "description": "Company A - ведущий производитель электроники."},
    "2": {"name": "Company B", "description": "Company B - глобальная торговая сеть."},
    "3": {"name": "Company C", "description": "Company C - инновационный стартап в сфере ИИ."}
}


# Инициализация "Dispatcher" для обработки апдейтов Telegram
# Dispatcher обычно создаётся Updater-ом, но т.к. мы используем Flask, сделаем ручную инициализацию
from telegram import Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update: Update, context: CallbackContext):
    """Обработчик команды /start - показывает список компаний."""
    keyboard = []
    for cid, cinfo in COMPANIES.items():
        keyboard.append([InlineKeyboardButton(cinfo["name"], callback_data=f"company_{cid}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите компанию:", reply_markup=reply_markup)

def company_details(update: Update, context: CallbackContext):
    """Обработчик нажатия на кнопку компании - показывает детали."""
    query = update.callback_query
    query.answer()
    
    data = query.data
    # data в формате "company_1"
    cid = data.split("_")[1]
    company = COMPANIES.get(cid)
    if company:
        text = f"Название: {company['name']}\nОписание: {company['description']}"
        query.edit_message_text(text=text)
    else:
        query.edit_message_text(text="Компания не найдена.")

# Регистрация хэндлеров
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(company_details, pattern="^company_"))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Функция приёма обновлений от Telegram."""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return "Бот работает!", 200

if __name__ == '__main__':
    # Запуск Flask-приложения
    # В продакшне используйте gunicorn или uwsgi + Nginx (HTTPS).
    # Для тестов локально - просто:
    # ВНИМАНИЕ: webhook будет работать только при публичном доступе, локально можно использовать ngrok.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))

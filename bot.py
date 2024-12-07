from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN

# Инициализируем бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update: Update, context: CallbackContext):
    # URL вашего приложения
    webapp_url = "https://ваш_домен/webapp"

    # Кнопка для открытия WebApp
    keyboard = [
        [
            InlineKeyboardButton("Открыть приложение", web_app={"url": webapp_url})
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    update.message.reply_text("Нажмите кнопку ниже, чтобы открыть приложение:", reply_markup=reply_markup)

def send_webapp_link(update: Update, context: CallbackContext):
    webapp_url = "https://goody-bot.onrender.com/webapp"
    keyboard = [[InlineKeyboardButton("Открыть WebApp", web_app={"url": webapp_url})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Нажмите для открытия WebApp:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("webapp", send_webapp_link))

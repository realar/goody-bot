from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN

# Инициализируем бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update: Update, context: CallbackContext):
    # URL вашего приложения
    webapp_url = "https://goody-bot.onrender.com/webapp"

    # Кнопка для открытия WebApp
    keyboard = [
        [
            InlineKeyboardButton("Открыть приложение", web_app={"url": webapp_url})
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    update.message.reply_text("Привет! Это команда Гуди Авто ❤️\n\n"
    "Мы создали платформу в Telegram, которая помогает находить проверенные компании для покупки авто с аукционов разных стран.\n\n"
    "🚗 *Почему стоит выбрать Goody Auto?*\n"
    "⭐️ Подбирай лучшие предложения с аукционов Японии, Кореи, США и других стран.\n"
    "⭐️ Общайся только с проверенными компаниями.\n"
    "⭐️ Получай актуальную информацию и советы по выбору автомобиля.\n\n"
    "Ты среди первых, кто получает доступ к нашей платформе!\n\n"
    "Твое мнение важно для нас – помогай развивать платформу и получай 🧡 бонусы за вклад.\n\n"
    "Нажми кнопку *Открыть приложение*, чтобы начать поиск своего идеального авто! 🚀", reply_markup=reply_markup)

def send_webapp_link(update: Update, context: CallbackContext):
    webapp_url = "https://goody-bot.onrender.com/webapp"
    keyboard = [[InlineKeyboardButton("Открыть WebApp", web_app={"url": webapp_url})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Нажмите для открытия WebApp:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("webapp", send_webapp_link))

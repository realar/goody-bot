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
    update.message.reply_text("Привет! Это Гуди Авто ❤️

Мы создали платформу в Telegram, которая помогает находить проверенные компании для покупки авто с аукционов разных стран.

🚗 Почему стоит выбрать Goody Auto?
⭐️ Подбирай лучшие предложения с аукционов Японии, Кореи, США и других стран.
⭐️ Общайся только с проверенными компаниями.
⭐️ Получай актуальную информацию и советы по выбору автомобиля.

Ты среди первых, кто получает доступ к нашей платформе!

Твое мнение важно для нас – помогай развивать платформу и получай 🧡 бонусы за вклад.

Нажми "Открыть приложение", чтобы начать поиск своего идеального авто! 🚀", reply_markup=reply_markup)

def send_webapp_link(update: Update, context: CallbackContext):
    webapp_url = "https://goody-bot.onrender.com/webapp"
    keyboard = [[InlineKeyboardButton("Открыть WebApp", web_app={"url": webapp_url})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Нажмите для открытия WebApp:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("webapp", send_webapp_link))

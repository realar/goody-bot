from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN

# Инициализируем бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    # URL вашего Web App
    webapp_url = "https://goody-bot.onrender.com/webapp"
    image_url = "https://5koleso.ru/wp-content/uploads/2022/06/changan_67.jpg"  # Ссылка на изображение

    # Создание кнопки для открытия Web App
    keyboard = [
        [
            InlineKeyboardButton("Открыть приложение", web_app={"url": webapp_url})  # Кнопка для Web App
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с изображением и текстом
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=(
            "Привет! Это команда Гуди Авто ❤️\n\n"
            "Мы создали платформу в Telegram, которая помогает находить проверенные компании для покупки авто с аукционов разных стран.\n\n"
            "🚗 *Почему стоит выбрать Goody Auto?*\n"
            "⭐️ Подбирай лучшие предложения с аукционов Японии, Кореи, США и других стран.\n"
            "⭐️ Общайся только с проверенными компаниями.\n"
            "⭐️ Получай актуальную информацию и советы по выбору автомобиля.\n\n"
            "Ты среди первых, кто получает доступ к нашей платформе!\n\n"
            "Твое мнение важно для нас – помогай развивать платформу и получай 🧡 бонусы за вклад.\n\n"
            "Наш канал с новостями – t.me/gudiauto\n\n"
            "Нажми кнопку *Открыть приложение*, чтобы начать поиск своего идеального авто! 🚀"
        ),
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Дополнительный обработчик команды /webapp
def send_webapp_link(update: Update, context: CallbackContext):
    webapp_url = "https://goody-bot.onrender.com/webapp"

    # Создание кнопки для открытия Web App
    keyboard = [
        [
            InlineKeyboardButton("Открыть WebApp", web_app={"url": webapp_url})
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка сообщения с кнопкой
    update.message.reply_text("Нажмите для открытия WebApp:", reply_markup=reply_markup)

# Регистрируем обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("webapp", send_webapp_link))

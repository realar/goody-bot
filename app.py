import os
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

# Токен бота
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

app = Flask(__name__)

# Данные о компаниях
COMPANIES = {
    "1": {"name": "Company A", "description": "Company A - ведущий производитель электроники."},
    "2": {"name": "Company B", "description": "Company B - глобальная торговая сеть."},
    "3": {"name": "Company C", "description": "Company C - инновационный стартап в сфере ИИ."}
}

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update, context):
    update.message.reply_text("Привет! Наберите /webapp чтобы получить ссылку на WebApp.")

def send_webapp_link(update, context):
    # Кнопка, открывающая WebApp
    keyboard = [[InlineKeyboardButton("Открыть WebApp", web_app={"url": f"https://{request.host}/webapp"})]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Нажмите для открытия WebApp:", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("webapp", send_webapp_link))


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return "Бот работает!", 200


# Маршрут для данных о компаниях в формате JSON (для удобства)
@app.route('/api/companies')
def get_companies():
    # Возвращаем простые данные о компаниях
    return jsonify(COMPANIES)


@app.route('/webapp')
def webapp_page():
    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Гуди - Компании</title>
<style>
    body, html {
        margin: 0; padding: 0;
        font-family: sans-serif;
        background: #fff;
        color: #000;
    }
    /* Шапка */
    .header {
        height: 48px;
        margin: 16px;
        display: flex;
        align-items: center;
        background: #000;
        color: #fff;
        padding: 0px 16px;
        border-radius: 12px;
    }
    .header-logo {
        font-size: 20px;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
    .header-logo::before {
        content: "❞";
        font-size: 20px;
        margin-right: 5px;
        transform: rotate(180deg);
        display: inline-block;
    }
    .header-spacer {
        flex: 1;
    }
    .header-menu {
        width: 24px;
        height: 24px;
        background: no-repeat center/contain url('data:image/svg+xml,%3Csvg width="24" height="24" viewBox="0 0 24 24" fill="%23fff" xmlns="http://www.w3.org/2000/svg"%3E%3Crect x="3" y="5" width="18" height="2" rx="1" fill="%23fff"/%3E%3Crect x="3" y="11" width="18" height="2" rx="1" fill="%23fff"/%3E%3Crect x="3" y="17" width="18" height="2" rx="1" fill="%23fff"/%3E%3C/svg%3E');
    }

    /* Строка для выбора страны аукциона */
    .country-select {
        height: 40px;
        margin: 16px;
        background: #eaeaea;
        padding: 0px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 14px;
        color: #333;
        border-radius: 12px;
    }
    .country-select-text {
        opacity: 0.7;
    }
    .country-select-arrow {
        width: 14px;
        height: 14px;
        background: no-repeat center/contain url('data:image/svg+xml,%3Csvg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"%3E%3Cpath d="M4.08331 5.16667L7.00065 8.08333L9.91798 5.16667" stroke="%23999" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/%3E%3C/svg%3E');
        opacity: 0.7;
    }

    /* Основной контент */
    .content {
        padding: 20px;
        font-size: 20px;
        line-height: 1.4;
    }

</style>
</head>
<body>
    <div class="header">
        <div class="header-logo">гуди</div>
        <div class="header-spacer"></div>
        <div class="header-menu"></div>
    </div>

    <div class="country-select">
        <div class="country-select-text">Страна аукциона</div>
        <div class="country-select-arrow"></div>
    </div>

    <div class="content">
        Пока что здесь нет компаний,<br>но мы над этим работаем!
    </div>

<script>
    const tg = window.Telegram.WebApp;
    tg.expand();
    tg.ready();

    // Подстройка цветов под тему Telegram (если нужно)
    const themeParams = tg.themeParams;
    // Пример (можно убрать если не требуется темизация):
    // document.body.style.backgroundColor = themeParams.bg_color || '#fff';
    // document.body.style.color = themeParams.text_color || '#000';
</script>
</body>
</html>
    """
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))

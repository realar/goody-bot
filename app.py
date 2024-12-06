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
    # Простая HTML-страница, интегрированная с Telegram WebApp
    # Используем window.Telegram.WebApp для получения цветовой схемы, настроек темы
    # Минимальный интерфейс: список компаний и блок деталей
    html = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Companies WebApp</title>
<style>
    body {
        font-family: sans-serif;
        margin: 0; padding: 0;
        background: #f9f9f9;
        color: #333;
    }
    header {
        background: #0088cc;
        color: #fff;
        padding: 10px;
        text-align: center;
    }
    .container {
        padding: 10px;
    }
    .company-list, .company-details {
        margin-bottom: 20px;
    }
    .company-item {
        background: #fff;
        border: 1px solid #ddd;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
    }
    .company-item:hover {
        background: #eee;
    }
    .details {
        background: #fff;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .back-button {
        display: none;
        margin-bottom: 10px;
        cursor: pointer;
        color: #0088cc;
        text-decoration: underline;
    }
</style>
</head>
<body>
    <header>
        <h1>Список компаний</h1>
    </header>
    <div class="container">
        <div class="company-list" id="company-list">
            Загрузка компаний...
        </div>
        <div class="back-button" id="back-button">← Назад</div>
        <div class="company-details" id="company-details" style="display:none;"></div>
    </div>

<script>
    // Работаем с Telegram WebApp API
    const tg = window.Telegram.WebApp;
    tg.expand(); // Расширяем на весь экран

    // Загрузка списка компаний
    fetch('/api/companies')
      .then(response => response.json())
      .then(data => {
          const listEl = document.getElementById('company-list');
          listEl.innerHTML = '';
          for (const cid in data) {
              const item = document.createElement('div');
              item.className = 'company-item';
              item.textContent = data[cid].name;
              item.onclick = () => showDetails(cid, data[cid]);
              listEl.appendChild(item);
          }
      });

    const detailsEl = document.getElementById('company-details');
    const backBtn = document.getElementById('back-button');
    const listEl = document.getElementById('company-list');

    function showDetails(cid, company) {
        detailsEl.innerHTML = '';
        const div = document.createElement('div');
        div.className = 'details';
        div.innerHTML = '<h2>' + company.name + '</h2><p>' + company.description + '</p>';
        detailsEl.appendChild(div);
        detailsEl.style.display = 'block';
        listEl.style.display = 'none';
        backBtn.style.display = 'block';
    }

    backBtn.onclick = () => {
        detailsEl.style.display = 'none';
        listEl.style.display = 'block';
        backBtn.style.display = 'none';
    };

    // Настройка цветов из темы Telegram
    const themeParams = tg.themeParams;
    document.body.style.backgroundColor = themeParams.bg_color || '#f9f9f9';
    document.body.style.color = themeParams.text_color || '#333';

    const header = document.querySelector('header');
    if (themeParams.header_color) {
        header.style.backgroundColor = themeParams.header_color;
    }

    // Когда WebApp готов - сообщим Telegram
    tg.ready();
</script>
</body>
</html>
    """
    return html, 200, {'Content-Type': 'text/html; charset=utf-8'}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))

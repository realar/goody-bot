import requests
from flask import Flask, request, render_template
from telegram import Update
from bot import bot, dispatcher
from webapp.routes import webapp_bp
from config import HOST, PORT

app = Flask(__name__, static_folder='webapp/static')
app.register_blueprint(webapp_bp)  # Регистрируем blueprint веб-приложения

BASE_URL = "https://api.baserow.io/api"
TOKEN = "jCemNYEzlw9FlzKGNElvoAbh6o2gbFc4"  # Ваш токен
table_id = 403967       # Ваш table_id

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    response = requests.get(
        f"{BASE_URL}/database/rows/table/{table_id}/",
        headers={"Authorization": f"Token {TOKEN}"}
    )

    if response.status_code == 200:
        data = response.json()['results']
        # data - это список словарей. Каждый словарь — запись компании
        # Например, data[0]['Name'] может быть названием компании,
        # если такое поле есть в таблице.

        return render_template('index.html', companies=data)
    else:
        return f"Error: {response.status_code} {response.text}", 500

@app.route('/autos')
def autos():
    return render_template('autos.html', title="Авто в наличии")

@app.route('/calc')
def calc():
    return render_template('calc.html', title="Калькулятор")

@app.route('/about')
def about():
    return render_template('about.html', title="О сервисе")

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

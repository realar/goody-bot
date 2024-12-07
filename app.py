from flask import Flask, request, render_template
from telegram import Update
from bot import bot, dispatcher
from webapp.routes import webapp_bp
from config import HOST, PORT

app = Flask(__name__)
app.register_blueprint(webapp_bp)  # Регистрируем blueprint веб-приложения

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def index():
    return render_template('index.html', title="Каталог компаний")

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

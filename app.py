from flask import Flask, request
from telegram import Update
from bot import bot, dispatcher
from webapp.routes import webapp_bp
from config import HOST, PORT

app = Flask(__name__)
app.register_blueprint(webapp_bp)  # Регистрируем blueprint веб-приложения

@app.route('/')
def index():
    return "Бот работает!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

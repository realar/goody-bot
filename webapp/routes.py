import requests 
from flask import Blueprint, render_template, jsonify

def fetch_companies_from_api():
    BASE_URL = "https://api.baserow.io/api"  # Пример API
    TOKEN = "ВАШ_ТОКЕН"
    TABLE_ID = "ВАШ_TABLE_ID"

    response = requests.get(
        f"{BASE_URL}/database/rows/table/{TABLE_ID}/",
        headers={"Authorization": f"Token {TOKEN}"}
    )
    if response.status_code == 200:
        # Преобразуем API-ответ в удобный формат
        companies = [
            {
                "name": item.get("field_3083783"),  # Имя компании
                "description": item.get("field_3083784")  # Описание
            }
            for item in response.json().get("results", [])
        ]
        return companies
    else:
        print(f"Ошибка API: {response.status_code} - {response.text}")
        return []

webapp_bp = Blueprint(
    'webapp', __name__,
    template_folder='templates',
    static_folder='static'
)

@webapp_bp.route('/webapp')
def webapp_page():
    companies = fetch_companies_from_api()  # Получаем данные из API
    return render_template('index.html', companies=companies)

@webapp_bp.route('/api/companies')
def get_companies():
    return jsonify(COMPANIES)

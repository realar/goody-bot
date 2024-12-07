import requests 
from flask import Blueprint, render_template, jsonify

def fetch_companies_from_api():
    BASE_URL = "https://api.baserow.io/api"  # Пример API
    TOKEN = "jCemNYEzlw9FlzKGNElvoAbh6o2gbFc4"
    TABLE_ID = 403967

    response = requests.get(
        f"{BASE_URL}/database/rows/table/{TABLE_ID}/",
        headers={"Authorization": f"Token {TOKEN}"}
    )
    if response.status_code == 200:
        # Преобразуем API-ответ в удобный формат
        companies = [
            {
                "id": item.get("id"),
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
    try:
        companies = fetch_companies_from_api()  # Получаем данные из API
        if not companies:
            companies = [{"name": "Нет данных", "description": "Попробуйте позже."}]
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        companies = [{"name": "Ошибка", "description": "Не удалось загрузить компании."}]
    return render_template('index.html', companies=companies)

@webapp_bp.route('/api/companies')
def get_companies():
    try:
        companies = fetch_companies_from_api()  # Загружаем данные из базы
        return jsonify(companies)
    except Exception as e:
        print(f"Ошибка при загрузке данных из API: {e}")
        return jsonify({"error": "Не удалось загрузить данные"}), 500

@webapp_bp.route('/company/<int:company_id>')
def company_details(company_id):
    companies = fetch_companies_from_api()
    company = next((comp for comp in companies if comp['id'] == company_id), None)
    if not company:
        return render_template('404.html'), 404
    return render_template('company_details.html', company=company)

from flask import Blueprint, render_template, jsonify
# Предположим, у нас есть данные о компаниях в этом же файле или импортируем их откуда-то ещё
COMPANIES = {
    "1": {"name": "Company A", "description": "Company A - ведущий производитель электроники."},
    "2": {"name": "Company B", "description": "Company B - глобальная торговая сеть."},
    "3": {"name": "Company C", "description": "Company C - инновационный стартап в сфере ИИ."}
}

webapp_bp = Blueprint(
    'webapp', __name__,
    template_folder='templates',
    static_folder='static'
)

@webapp_bp.route('/webapp')
def webapp_page():
    return render_template('index.html', companies=COMPANIES)

@webapp_bp.route('/api/companies')
def get_companies():
    return jsonify(COMPANIES)

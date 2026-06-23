from flask import Blueprint, request, jsonify
from services.bailian_service import generate_and_execute_sql

ai_query_bp = Blueprint('ai_query', __name__)


@ai_query_bp.route('/api/ai-query', methods=['POST'])
def ai_query():
    data = request.get_json()
    question = data.get('question', '')
    result = generate_and_execute_sql(question)
    return jsonify(result)

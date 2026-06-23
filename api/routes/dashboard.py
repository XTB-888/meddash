from flask import Blueprint, request, jsonify
from services.dashboard_service import get_dashboard_data

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def dashboard():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    department = request.args.get('department')
    
    data = get_dashboard_data(start_date, end_date, department)
    return jsonify(data)

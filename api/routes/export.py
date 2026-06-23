from flask import Blueprint, request, make_response
from services.export_service import export_data

export_bp = Blueprint('export', __name__)

@export_bp.route('/api/export', methods=['GET'])
def export():
    data_type = request.args.get('type', 'all')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    department = request.args.get('department')
    
    csv_data = export_data(data_type, start_date, end_date, department)
    
    output = make_response(csv_data)
    output.headers["Content-Disposition"] = f"attachment; filename={data_type}_export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

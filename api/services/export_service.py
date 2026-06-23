import csv
from io import StringIO
from datetime import datetime, timedelta
from database import get_db


def export_data(data_type, start_date=None, end_date=None, department=None):
    conn = get_db()
    cursor = conn.cursor()

    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    dept_condition = ''
    params = [start_date, end_date]
    if department:
        dept_condition = ' AND d.name = ?'
        params.append(department)

    if data_type == 'outpatient':
        cursor.execute(f'''
            SELECT
                o.date,
                d.name as department,
                o.count,
                o.emergency_count
            FROM outpatients o
            JOIN departments d ON o.department_id = d.id
            WHERE o.date BETWEEN ? AND ?{dept_condition}
            ORDER BY o.date DESC
        ''', params)
        rows = cursor.fetchall()
        headers = ['日期', '科室', '门诊量', '急诊量']
    elif data_type == 'revenue':
        cursor.execute(f'''
            SELECT
                r.date,
                d.name as department,
                r.type,
                r.amount
            FROM revenues r
            JOIN departments d ON r.department_id = d.id
            WHERE r.date BETWEEN ? AND ?{dept_condition}
            ORDER BY r.date DESC
        ''', params)
        rows = cursor.fetchall()
        headers = ['日期', '科室', '类型', '金额']
    else:
        cursor.execute(f'''
            SELECT
                o.date,
                d.name as department,
                o.count as outpatient_count,
                o.emergency_count,
                SUM(r.amount) as total_revenue
            FROM outpatients o
            LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
            JOIN departments d ON o.department_id = d.id
            WHERE o.date BETWEEN ? AND ?{dept_condition}
            GROUP BY o.date, o.department_id
            ORDER BY o.date DESC
        ''', params)
        rows = cursor.fetchall()
        headers = ['日期', '科室', '门诊量', '急诊量', '总收入']

    conn.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)

    for row in rows:
        if isinstance(row, dict):
            values = [row[key] for key in headers]
        else:
            values = [row[i] for i in range(len(headers))]
        writer.writerow(values)

    return output.getvalue()

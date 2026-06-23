import random
from database import get_db
from datetime import datetime, timedelta


def get_dashboard_data(start_date=None, end_date=None, department=None):
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

    cursor.execute(f'''
        SELECT
            COALESCE(SUM(o.count), 0) as total_outpatient,
            COALESCE(SUM(r.amount), 0) as total_revenue
        FROM outpatients o
        LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
        JOIN departments d ON o.department_id = d.id
        WHERE o.date BETWEEN ? AND ?{dept_condition}
    ''', params)
    overview = cursor.fetchone()

    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    dept_today = [today] + ([department] if department else [])
    cursor.execute(f'''
        SELECT
            COALESCE(SUM(o.count), 0) as today_outpatient,
            COALESCE(SUM(r.amount), 0) as today_revenue
        FROM outpatients o
        LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
        JOIN departments d ON o.department_id = d.id
        WHERE o.date = ?{dept_condition}
    ''', dept_today)
    today_data = cursor.fetchone()

    dept_yesterday = [yesterday] + ([department] if department else [])
    cursor.execute(f'''
        SELECT
            COALESCE(SUM(o.count), 0) as yesterday_outpatient,
            COALESCE(SUM(r.amount), 0) as yesterday_revenue
        FROM outpatients o
        LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
        JOIN departments d ON o.department_id = d.id
        WHERE o.date = ?{dept_condition}
    ''', dept_yesterday)
    yesterday_data = cursor.fetchone()

    daily_outpatient = today_data['today_outpatient'] or 0
    daily_revenue = today_data['today_revenue'] or 0
    yesterday_outpatient = yesterday_data['yesterday_outpatient'] or 1
    yesterday_revenue = yesterday_data['yesterday_revenue'] or 1

    outpatient_change = ((daily_outpatient - yesterday_outpatient) / yesterday_outpatient) * 100
    revenue_change = ((daily_revenue - yesterday_revenue) / yesterday_revenue) * 100

    cursor.execute(f'''
        SELECT
            o.date,
            SUM(o.count) as outpatient_count,
            SUM(r.amount) as revenue
        FROM outpatients o
        LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
        JOIN departments d ON o.department_id = d.id
        WHERE o.date BETWEEN ? AND ?{dept_condition}
        GROUP BY o.date
        ORDER BY o.date
    ''', params)
    trends = cursor.fetchall()

    cursor.execute(f'''
        SELECT
            d.name,
            SUM(o.count) as outpatient_count,
            SUM(r.amount) as revenue
        FROM outpatients o
        LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
        JOIN departments d ON o.department_id = d.id
        WHERE o.date BETWEEN ? AND ?{dept_condition}
        GROUP BY d.id, d.name
        ORDER BY revenue DESC
    ''', params)
    departments = cursor.fetchall()

    conn.close()

    return {
        'overview': {
            'dailyOutpatient': int(daily_outpatient),
            'totalRevenue': float(daily_revenue),
            'inHospital': 120 + random.randint(-30, 50),
            'outpatientChange': round(outpatient_change, 1),
            'revenueChange': round(revenue_change, 1),
        },
        'trends': {
            'dates': [t['date'] for t in trends],
            'outpatientCounts': [int(t['outpatient_count'] or 0) for t in trends],
            'revenues': [float(t['revenue'] or 0) for t in trends],
        },
        'departments': [
            {
                'name': d['name'],
                'outpatientCount': int(d['outpatient_count'] or 0),
                'revenue': float(d['revenue'] or 0),
            }
            for d in departments
        ],
    }

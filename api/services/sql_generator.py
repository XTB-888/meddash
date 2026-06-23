from database import get_db
import re

def generate_and_execute_sql(question):
    question_lower = question.lower()
    
    sql = ''
    chart_type = 'bar'
    explanation = ''
    
    if '内科' in question and '收入' in question:
        sql = '''
            SELECT 
                date,
                SUM(amount) as total_revenue
            FROM revenues r
            JOIN departments d ON r.department_id = d.id
            WHERE d.name = '内科'
            GROUP BY date
            ORDER BY date
        '''
        chart_type = 'line'
        explanation = '查询内科近期收入趋势'
    elif '科室' in question and '门诊' in question:
        sql = '''
            SELECT 
                d.name,
                SUM(o.count) as total_outpatient
            FROM outpatients o
            JOIN departments d ON o.department_id = d.id
            GROUP BY d.id, d.name
            ORDER BY total_outpatient DESC
        '''
        chart_type = 'bar'
        explanation = '对比各科室门诊量'
    elif '收入' in question and '趋势' in question:
        sql = '''
            SELECT 
                date,
                SUM(amount) as total_revenue
            FROM revenues
            GROUP BY date
            ORDER BY date
        '''
        chart_type = 'line'
        explanation = '查看整体收入趋势'
    elif '急诊' in question:
        sql = '''
            SELECT 
                d.name,
                SUM(o.emergency_count) as total_emergency
            FROM outpatients o
            JOIN departments d ON o.department_id = d.id
            GROUP BY d.id, d.name
            ORDER BY total_emergency DESC
        '''
        chart_type = 'pie'
        explanation = '统计各科室急诊量分布'
    else:
        sql = '''
            SELECT 
                date,
                SUM(o.count) as outpatient_count,
                SUM(r.amount) as revenue
            FROM outpatients o
            LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
            GROUP BY date
            ORDER BY date DESC
            LIMIT 30
        '''
        chart_type = 'line'
        explanation = '默认展示最近30天门诊量和收入趋势'
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    
    result_list = [dict(row) for row in results]
    
    return {
        'sql': sql.strip(),
        'result': result_list,
        'chartType': chart_type,
        'explanation': explanation
    }

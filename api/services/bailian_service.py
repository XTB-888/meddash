import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv
from database import get_db

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)


DATABASE_SCHEMA = '''
数据库表结构:
1. departments (科室表): id, name (科室名称), description
2. outpatients (门诊表): id, department_id, date, count (门诊量), emergency_count (急诊量)
3. revenues (收入表): id, department_id, date, amount (金额), type (收入类型: 挂号费/诊疗费/药费/检查费)

可用科室: 内科, 外科, 儿科, 妇产科, 急诊科

SQLite 语法规范:
- 使用 SUM(), COUNT(), AVG() 等聚合函数
- JOIN departments d ON ... 连接科室表
- WHERE 条件: date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'
- GROUP BY / ORDER BY 排序
- LIMIT 限制返回条数
- 使用 COALESCE(column, 0) 处理 NULL 值
'''


def get_bailian_api_key():
    return os.environ.get('DASHSCOPE_API_KEY', '')


def call_bailian_llm(prompt, system_prompt=None):
    api_key = get_bailian_api_key()
    if not api_key:
        return None

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    body = {
        "model": "qwen-plus",
        "input": {"messages": messages},
        "parameters": {"temperature": 0.3, "top_p": 0.8, "max_tokens": 1024},
    }

    try:
        data = json.dumps(body).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

            if 'output' in result:
                if 'text' in result['output']:
                    return result['output']['text']
                elif 'choices' in result['output'] and len(result['output']['choices']) > 0:
                    return result['output']['choices'][0]['message']['content']
            return None
    except Exception as e:
        print(f"[Bailian] API call failed: {e}")
        return None


def generate_sql_with_llm(question):
    system_prompt = '''你是一个专业的医疗数据分析师，擅长将用户的自然语言问题转换为精准的SQL查询语句。

请根据用户的问题，只输出SQL语句，不要包含任何解释、反引号或其他文字。

选择合适的图表类型来可视化查询结果：
- line: 时间序列趋势分析
- bar: 分类对比、排名
- pie: 占比、分布分析

请严格按照以下JSON格式返回（只返回JSON，不要其他内容）：
{"sql": "SELECT ...", "chartType": "line|bar|pie", "explanation": "简洁的中文解释"}

注意：
- 必须使用SQLite语法
- 必须涉及departments, outpatients, revenues表
- 中文科室名必须用正确的条件过滤
- 按日期查询要用 date 字段
- 不要输出markdown，只输出纯JSON字符串
'''

    prompt = f'''用户问题: "{question}"

请生成对应的SQL查询语句。

{DATABASE_SCHEMA}'''

    response = call_bailian_llm(prompt, system_prompt)

    if not response:
        return None

    try:
        cleaned = response.strip()
        if cleaned.startswith('```') and cleaned.endswith('```'):
            cleaned = cleaned[3:-3].strip()
        if cleaned.startswith('json'):
            cleaned = cleaned[4:].strip()

        result = json.loads(cleaned)
        return result
    except (json.JSONDecodeError, Exception) as e:
        print(f"[Bailian] Failed to parse LLM response: {e}")
        return None


def execute_query(sql):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"[Bailian] SQL execution failed: {e}")
        return []


def fallback_sql_generator(question):
    q = question.lower()

    sql = '''
        SELECT
            o.date,
            SUM(o.count) as outpatient_count,
            SUM(r.amount) as revenue
        FROM outpatients o
        LEFT JOIN revenues r ON o.department_id = r.department_id AND o.date = r.date
        GROUP BY o.date
        ORDER BY o.date DESC
        LIMIT 30
    '''
    chart_type = 'line'
    explanation = '为您展示最近30天的门诊量和收入趋势数据'

    if any(kw in question for kw in ['内科', '外科', '儿科', '妇产科', '急诊']):
        dept_name = None
        for d in ['内科', '外科', '儿科', '妇产科', '急诊科']:
            if d in question:
                dept_name = d
                break

        if dept_name:
            if any(kw in question for kw in ['收入', '金额', '费用']):
                sql = f'''
                    SELECT
                        r.date,
                        SUM(r.amount) as total_revenue,
                        d.name as department
                    FROM revenues r
                    JOIN departments d ON r.department_id = d.id
                    WHERE d.name = '{dept_name}'
                    GROUP BY r.date
                    ORDER BY r.date DESC
                    LIMIT 60
                '''
                chart_type = 'line'
                explanation = f'{dept_name}近期收入趋势分析'
            elif any(kw in question for kw in ['门诊', '就诊', '挂号']):
                sql = f'''
                    SELECT
                        o.date,
                        SUM(o.count) as total_outpatient,
                        d.name as department
                    FROM outpatients o
                    JOIN departments d ON o.department_id = d.id
                    WHERE d.name = '{dept_name}'
                    GROUP BY o.date
                    ORDER BY o.date DESC
                    LIMIT 60
                '''
                chart_type = 'line'
                explanation = f'{dept_name}近期门诊量变化趋势'
            elif any(kw in question for kw in ['急诊', '急救']):
                sql = f'''
                    SELECT
                        o.date,
                        SUM(o.emergency_count) as total_emergency,
                        d.name as department
                    FROM outpatients o
                    JOIN departments d ON o.department_id = d.id
                    WHERE d.name = '{dept_name}'
                    GROUP BY o.date
                    ORDER BY o.date DESC
                    LIMIT 60
                '''
                chart_type = 'line'
                explanation = f'{dept_name}近期急诊量统计'

    elif any(kw in question for kw in ['科室', '对比', '排名', 'TOP', 'top']):
        if any(kw in question for kw in ['收入', '金额']):
            sql = '''
                SELECT
                    d.name,
                    SUM(r.amount) as total_revenue
                FROM revenues r
                JOIN departments d ON r.department_id = d.id
                GROUP BY d.id, d.name
                ORDER BY total_revenue DESC
            '''
            chart_type = 'bar'
            explanation = '各科室收入排名对比'
        else:
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
            explanation = '各科室门诊量排名对比'

    elif any(kw in question for kw in ['占比', '分布', '比例', '构成']):
        sql = '''
            SELECT
                d.name,
                SUM(r.amount) as total_revenue
            FROM revenues r
            JOIN departments d ON r.department_id = d.id
            GROUP BY d.id, d.name
            ORDER BY total_revenue DESC
        '''
        chart_type = 'pie'
        explanation = '各科室收入占比分布'

    elif any(kw in question for kw in ['趋势', '变化', '走势', '时间']):
        if any(kw in question for kw in ['收入', '金额']):
            sql = '''
                SELECT
                    date,
                    SUM(amount) as total_revenue
                FROM revenues
                GROUP BY date
                ORDER BY date DESC
                LIMIT 60
            '''
            chart_type = 'line'
            explanation = '全院收入趋势变化'
        else:
            sql = '''
                SELECT
                    date,
                    SUM(count) as total_outpatient
                FROM outpatients
                GROUP BY date
                ORDER BY date DESC
                LIMIT 60
            '''
            chart_type = 'line'
            explanation = '全院门诊量趋势变化'

    return {
        'sql': sql.strip(),
        'chartType': chart_type,
        'explanation': explanation,
    }


def generate_and_execute_sql(question):
    api_key = get_bailian_api_key()

    if api_key:
        print(f"[Bailian] Using Aliyun Bailian LLM for query: {question}")
        llm_result = generate_sql_with_llm(question)

        if llm_result and 'sql' in llm_result:
            sql = llm_result['sql']
            chart_type = llm_result.get('chartType', 'line')
            explanation = llm_result.get('explanation', 'AI智能分析结果')

            results = execute_query(sql)

            if results and len(results) > 0:
                return {
                    'sql': sql,
                    'result': results,
                    'chartType': chart_type,
                    'explanation': explanation,
                }

    print(f"[Bailian] Using fallback rule-based SQL generator")
    fallback = fallback_sql_generator(question)
    results = execute_query(fallback['sql'])

    return {
        'sql': fallback['sql'],
        'result': results,
        'chartType': fallback['chartType'],
        'explanation': f"{fallback['explanation']}（使用规则引擎，配置API key后可启用AI智能分析）",
    }

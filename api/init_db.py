import random
import math
from datetime import datetime, timedelta
from database import get_db, init_db


def get_season_factor(date):
    month = date.month
    if month in [12, 1, 2]:
        return 1.3
    elif month in [3, 4, 5]:
        return 1.1
    elif month in [6, 7, 8]:
        return 0.85
    else:
        return 1.0


def get_weekend_factor(date):
    if date.weekday() >= 5:
        return 0.75
    return 1.0


def get_holiday_factor(date):
    holidays = [
        (1, 1), (1, 2), (1, 3),
        (5, 1), (5, 2), (5, 3),
        (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7),
    ]
    if (date.month, date.day) in holidays:
        return 0.6
    return 1.0


def get_flu_season_factor(date):
    if date.month in [11, 12, 1, 2, 3]:
        return 1.25
    return 1.0


def generate_sample_data():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT id, name FROM departments')
    departments = cursor.fetchall()

    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()

    cursor.execute('DELETE FROM outpatients')
    cursor.execute('DELETE FROM revenues')

    dept_base = {
        '内科': {'outpatient': 280, 'emergency_ratio': 0.08, 'revenue_base': 35000},
        '外科': {'outpatient': 200, 'emergency_ratio': 0.12, 'revenue_base': 45000},
        '儿科': {'outpatient': 220, 'emergency_ratio': 0.06, 'revenue_base': 22000},
        '妇产科': {'outpatient': 180, 'emergency_ratio': 0.05, 'revenue_base': 28000},
        '急诊科': {'outpatient': 150, 'emergency_ratio': 0.85, 'revenue_base': 50000},
        '眼科': {'outpatient': 120, 'emergency_ratio': 0.02, 'revenue_base': 18000},
        '口腔科': {'outpatient': 100, 'emergency_ratio': 0.01, 'revenue_base': 20000},
        '皮肤科': {'outpatient': 130, 'emergency_ratio': 0.01, 'revenue_base': 15000},
        '中医科': {'outpatient': 90, 'emergency_ratio': 0.01, 'revenue_base': 12000},
        '骨科': {'outpatient': 140, 'emergency_ratio': 0.10, 'revenue_base': 38000},
        '耳鼻喉科': {'outpatient': 110, 'emergency_ratio': 0.03, 'revenue_base': 16000},
        '泌尿外科': {'outpatient': 85, 'emergency_ratio': 0.04, 'revenue_base': 25000},
    }

    revenue_types = ['挂号费', '诊疗费', '药费', '检查费', '手术费', '住院费', '其他']
    revenue_ratios = {
        '挂号费': 0.05, '诊疗费': 0.15, '药费': 0.30, '检查费': 0.20, '手术费': 0.15, '住院费': 0.10, '其他': 0.05,
    }

    current_date = start_date
    total_outpatients = 0
    total_revenue = 0.0

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        season_factor = get_season_factor(current_date)
        weekend_factor = get_weekend_factor(current_date)
        holiday_factor = get_holiday_factor(current_date)
        flu_factor = get_flu_season_factor(current_date)

        for dept in departments:
            dept_id = dept['id']
            dept_name = dept['name']
            base = dept_base.get(dept_name, {'outpatient': 100, 'emergency_ratio': 0.05, 'revenue_base': 15000})

            day_factor = season_factor * weekend_factor * holiday_factor
            if dept_name in ['内科', '儿科', '急诊科']:
                day_factor *= flu_factor

            base_count = base['outpatient']
            random_variation = random.gauss(1.0, 0.15)
            count = max(10, int(base_count * day_factor * random_variation))
            emergency_count = max(1, int(count * base['emergency_ratio'] * random.gauss(1.0, 0.2)))

            cursor.execute('''
                INSERT INTO outpatients (department_id, date, count, emergency_count)
                VALUES (?, ?, ?, ?)
            ''', (dept_id, date_str, count, emergency_count))

            total_outpatients += count

            base_revenue = base['revenue_base']
            for rev_type in revenue_types:
                ratio = revenue_ratios[rev_type]
                rev_amount = round(base_revenue * ratio * day_factor * random.gauss(1.0, 0.2), 2)
                rev_amount = max(100.0, rev_amount)

                cursor.execute('''
                    INSERT INTO revenues (department_id, date, amount, type)
                    VALUES (?, ?, ?, ?)
                ''', (dept_id, date_str, rev_amount, rev_type))

                total_revenue += rev_amount

        current_date += timedelta(days=1)

    conn.commit()
    conn.close()

    days = (end_date - start_date).days + 1
    print('数据生成完成！')
    print(f'  时间范围: {start_date.strftime("%Y-%m-%d")} 至 {end_date.strftime("%Y-%m-%d")}')
    print(f'  天数: {days} 天')
    print(f'  科室数量: {len(departments)} 个')
    print(f'  门诊总量: {total_outpatients:,} 人次')
    print(f'  总收入: ¥{total_revenue:,.2f}')
    print(f'  日均门诊: {int(total_outpatients / days):,} 人次')
    print(f'  日均收入: ¥{total_revenue / days:,.2f}')


if __name__ == '__main__':
    generate_sample_data()

import random
from datetime import datetime, timedelta
from database import get_db, init_db

def generate_sample_data():
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM departments')
    department_ids = [row['id'] for row in cursor.fetchall()]
    
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
    
    cursor.execute('DELETE FROM outpatients')
    cursor.execute('DELETE FROM revenues')
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        
        for dept_id in department_ids:
            base_count = 50 + dept_id * 20
            count = random.randint(base_count - 20, base_count + 30)
            emergency_count = random.randint(5, 15)
            
            cursor.execute('''
                INSERT INTO outpatients (department_id, date, count, emergency_count)
                VALUES (?, ?, ?, ?)
            ''', (dept_id, date_str, count, emergency_count))
            
            for rev_type in ['挂号费', '诊疗费', '药费', '检查费']:
                base_amount = 5000 + dept_id * 2000 + random.randint(-1000, 2000)
                amount = round(base_amount * (0.5 + random.random()), 2)
                
                cursor.execute('''
                    INSERT INTO revenues (department_id, date, amount, type)
                    VALUES (?, ?, ?, ?)
                ''', (dept_id, date_str, amount, rev_type))
        
        current_date += timedelta(days=1)
    
    conn.commit()
    conn.close()
    print('Sample data generated successfully!')

if __name__ == '__main__':
    generate_sample_data()

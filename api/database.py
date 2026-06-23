import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hospital.db')

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS outpatients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER,
            date DATE NOT NULL,
            count INTEGER NOT NULL DEFAULT 0,
            emergency_count INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER,
            date DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
            type TEXT NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_outpatients_date ON outpatients(date)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_outpatients_dept ON outpatients(department_id)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_revenues_date ON revenues(date)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_revenues_dept ON revenues(department_id)
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM departments')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO departments (name, description) VALUES
            ('内科', '涵盖呼吸、消化、心血管等专业'),
            ('外科', '普通外科、骨科、神经外科等'),
            ('儿科', '儿童常见病、多发病诊疗'),
            ('妇产科', '妇科疾病、产科分娩等'),
            ('急诊科', '24小时急诊服务')
        ''')
    
    conn.commit()
    conn.close()

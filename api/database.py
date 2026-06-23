import sqlite3
import os

# 生产环境使用环境变量配置数据库路径
db_path = os.environ.get('DATABASE_PATH')
if db_path:
    DATABASE_PATH = db_path
else:
    # Railway 持久化存储路径
    railway_volume = os.environ.get('RAILWAY_VOLUME_MOUNT_PATH')
    if railway_volume:
        DATABASE_PATH = os.path.join(railway_volume, 'hospital.db')
    else:
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
            ('内科', '涵盖呼吸、消化、心血管、神经内科等专业'),
            ('外科', '普通外科、骨科、神经外科、胸外科等'),
            ('儿科', '儿童常见病、多发病诊疗，新生儿科'),
            ('妇产科', '妇科疾病、产科分娩、计划生育'),
            ('急诊科', '24小时急诊服务，急危重症抢救'),
            ('眼科', '眼科疾病诊治，视力矫正，白内障手术'),
            ('口腔科', '口腔疾病诊治，牙齿矫正，种植牙'),
            ('皮肤科', '皮肤病诊治，美容皮肤科'),
            ('中医科', '中医内科、针灸、推拿按摩'),
            ('骨科', '骨折、关节置换、脊柱外科'),
            ('耳鼻喉科', '耳、鼻、咽喉疾病诊治'),
            ('泌尿外科', '泌尿系统疾病，男科疾病')
        ''')
    
    conn.commit()
    conn.close()

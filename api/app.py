import os
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from routes.dashboard import dashboard_bp
from routes.ai_query import ai_query_bp
from routes.export import export_bp

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)

app = Flask(__name__)
CORS(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(ai_query_bp)
app.register_blueprint(export_bp)


@app.route('/')
def hello():
    api_key_status = '已配置' if os.environ.get('DASHSCOPE_API_KEY') else '未配置'
    return {
        'message': 'MedDash 医院运营数据看板 API Server',
        'version': '1.0.0',
        'ai_status': api_key_status,
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

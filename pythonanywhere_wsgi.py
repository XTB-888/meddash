import sys
import os

# Add your project directory to the sys.path
path = '/home/meddash/meddash'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

# Set environment variables
os.environ['DASHSCOPE_API_KEY'] = 'sk-49d3fc38cd8b4ed1be84354c47b6c05a'
os.environ['DATABASE_PATH'] = '/home/meddash/meddash/hospital.db'

# Import your Flask app
from api.app import app as application

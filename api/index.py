"""
Vercel Serverless Function Entry Point
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

# Vercel handler
from http.server import BaseHTTPRequestHandler
from io import BytesIO

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = app.test_client().get(self.path)
        self.wfile.write(response.data)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = app.test_client().post(self.path, data=body, content_type='application/json')
        self.wfile.write(response.data)

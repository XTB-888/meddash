#!/usr/bin/env python3
"""
MedDash 云端部署脚本
使用 ngrok 暴露本地服务到公网
"""
import os
import sys
import time
import subprocess
import signal
from pathlib import Path

def check_command(cmd):
    """检查命令是否存在"""
    return subprocess.run(['which', cmd], capture_output=True).returncode == 0

def install_ngrok():
    """安装 ngrok"""
    print("正在安装 ngrok...")
    if not check_command('ngrok'):
        # 下载 ngrok
        import urllib.request
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        urllib.request.urlretrieve(ngrok_url, "/tmp/ngrok.tgz")
        subprocess.run(["tar", "-xzf", "/tmp/ngrok.tgz", "-C", "/usr/local/bin"], check=True)
        print("ngrok 安装完成")
    else:
        print("ngrok 已安装")

def start_backend():
    """启动后端服务"""
    print("启动后端服务...")
    env = os.environ.copy()
    env['PORT'] = '5000'
    process = subprocess.Popen(
        [sys.executable, 'api/app.py'],
        cwd='/workspace',
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)
    return process

def start_frontend():
    """启动前端服务"""
    print("启动前端服务...")
    process = subprocess.Popen(
        ['npx', 'vite', 'preview', '--host', '0.0.0.0', '--port', '5173'],
        cwd='/workspace',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)
    return process

def start_ngrok_http(port):
    """启动 ngrok HTTP 隧道"""
    print(f"启动 ngrok 隧道 (端口 {port})...")
    process = subprocess.Popen(
        ['ngrok', 'http', str(port), '--log=stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(5)
    return process

def get_ngrok_url():
    """获取 ngrok 公网 URL"""
    try:
        import urllib.request
        import json
        with urllib.request.urlopen('http://localhost:4040/api/tunnels') as response:
            data = json.loads(response.read().decode())
            if data['tunnels']:
                return data['tunnels'][0]['public_url']
    except Exception as e:
        print(f"获取 ngrok URL 失败: {e}")
    return None

def main():
    print("=" * 60)
    print("MedDash 云端部署工具")
    print("=" * 60)

    # 安装 ngrok
    install_ngrok()

    # 检查 ngrok auth token
    ngrok_config = Path.home() / '.config/ngrok/ngrok.yml'
    if not ngrok_config.exists():
        print("\n警告: 未配置 ngrok auth token")
        print("请访问 https://dashboard.ngrok.com/get-started/your-authtoken 获取")
        print("然后运行: ngrok config add-authtoken YOUR_TOKEN")
        print("\n继续部署（可能有限制）...\n")

    # 启动服务
    backend = None
    frontend = None
    ngrok_backend = None
    ngrok_frontend = None

    try:
        # 启动后端
        backend = start_backend()

        # 启动前端
        frontend = start_frontend()

        # 启动 ngrok 隧道
        ngrok_backend = start_ngrok_http(5000)

        # 等待并获取 URL
        print("\n等待 ngrok 启动...")
        time.sleep(5)

        backend_url = get_ngrok_url()
        if backend_url:
            print(f"\n{'='*60}")
            print(f"后端 API 地址: {backend_url}")
            print(f"API 文档: {backend_url}/")
            print(f"{'='*60}\n")

        print("\n服务已启动！")
        print("按 Ctrl+C 停止服务")

        # 保持运行
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n正在停止服务...")
    finally:
        if ngrok_backend:
            ngrok_backend.terminate()
        if frontend:
            frontend.terminate()
        if backend:
            backend.terminate()
        print("服务已停止")

if __name__ == '__main__':
    main()

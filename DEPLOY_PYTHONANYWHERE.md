# PythonAnywhere 部署指南

## 步骤 1：注册账号
1. 访问 https://www.pythonanywhere.com/
2. 点击 **Start running Python online in less than a minute**
3. 填写用户名（建议 `meddash`）、邮箱、密码
4. 点击 **Create account**

## 步骤 2：上传代码
### 方法一：通过 Git 克隆
1. 登录后点击 **Consoles** → **Bash**
2. 运行以下命令：
```bash
cd ~
git clone https://github.com/XTB-888/meddash.git
cd meddash
pip install -r requirements.txt
cd api && python init_db.py
```

### 方法二：通过文件上传
1. 点击 **Files**
2. 上传项目 ZIP 文件并解压

## 步骤 3：配置 Web 应用
1. 点击 **Web** 标签
2. 点击 **Add a new web app**
3. 选择 **Manual configuration** → **Python 3.11**
4. 在 **Code** 部分：
   - **Source code**: `/home/meddash/meddash`
   - **Working directory**: `/home/meddash/meddash`
   - **WSGI configuration file**: 点击并编辑

5. 编辑 WSGI 文件，替换为以下内容：
```python
import sys
import os

path = '/home/meddash/meddash'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

os.environ['DASHSCOPE_API_KEY'] = 'sk-49d3fc38cd8b4ed1be84354c47b6c05a'
os.environ['DATABASE_PATH'] = '/home/meddash/meddash/hospital.db'
os.environ['ALLOWED_ORIGINS'] = '*'

from api.app import app as application
```

6. 点击 **Save**

## 步骤 4：配置虚拟环境
1. 点击 **Virtualenv** 部分的 **Enter path to a virtualenv**
2. 输入：`/home/meddash/.virtualenvs/meddash`
3. 在 Bash 控制台运行：
```bash
mkvirtualenv --python=/usr/bin/python3.11 meddash
pip install -r /home/meddash/meddash/requirements.txt
```

## 步骤 5：重启并访问
1. 点击 **Reload** 按钮
2. 访问地址：`https://meddash.pythonanywhere.com`

## 步骤 6：更新前端 API 地址
在 Vercel 前端的环境变量中设置：
- `VITE_API_BASE_URL` = `https://meddash.pythonanywhere.com/api`

## 注意事项
- 免费版每天限制 100 秒 CPU 时间
- 网站 24/7 在线，但首次访问可能稍慢
- 文件修改后需要点击 **Reload** 生效

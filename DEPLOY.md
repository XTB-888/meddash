# MedDash 云端部署指南

## 方案一：Render 部署（推荐）

Render 支持 Python + SQLite，免费套餐足够本项目使用。

### 1. 部署后端 API

1. 访问 [Render Dashboard](https://dashboard.render.com/)
2. 点击 **New +** → **Web Service**
3. 连接你的 GitHub 仓库
4. 配置如下：
   - **Name**: `meddash-api`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api.app:app --bind 0.0.0.0:$PORT --workers 2`
   - **Plan**: Free

5. 添加环境变量：
   - `DASHSCOPE_API_KEY`: 你的阿里云百炼 API Key
   - `DATABASE_PATH`: `hospital.db`

6. 添加磁盘（Persistent Disk）：
   - **Name**: `meddash-data`
   - **Mount Path**: `/opt/render/project/src`
   - **Size**: 1 GB

### 2. 部署前端（Vercel）

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 导入 GitHub 仓库
3. 配置：
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. 添加环境变量：
   - `VITE_API_BASE_URL`: `https://meddash-api.onrender.com/api`

### 3. 更新 CORS

部署后，修改 `api/app.py` 中的 CORS 配置，允许前端域名：

```python
CORS(app, origins=["https://your-frontend.vercel.app"])
```

---

## 方案二：Vercel 全栈部署

Vercel 支持 Python Serverless Functions，但 SQLite 数据不会持久化（每次部署重置）。

### 部署步骤

1. 确保 `vercel.json` 已配置
2. 安装 Vercel CLI: `npm i -g vercel`
3. 运行: `vercel --prod`
4. 设置环境变量: `vercel env add DASHSCOPE_API_KEY`

**注意**: Vercel 免费版的 Python 函数有 10 秒超时限制，且 SQLite 数据不持久化。适合演示，不适合生产。

---

## 方案三：Railway 部署

Railway 支持 Docker 部署，可以完整运行前后端。

### 部署步骤

1. 访问 [Railway](https://railway.app/)
2. 从 GitHub 部署
3. 添加环境变量
4. 自动生成域名

---

## 本地生产测试

在部署前，可以先本地测试生产构建：

```bash
# 1. 构建前端
npm run build

# 2. 安装生产依赖
pip install -r requirements.txt

# 3. 使用 gunicorn 启动后端
cd api && gunicorn app:app --bind 0.0.0.0:5000 --workers 2

# 4. 访问 http://localhost:5000
```

---

## 部署检查清单

- [ ] API Key 已配置到环境变量
- [ ] CORS 允许前端域名
- [ ] 数据库已初始化（`python api/init_db.py`）
- [ ] 前端 API 地址指向正确
- [ ] 测试所有功能正常

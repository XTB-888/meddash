# MedDash 快速启动指南

## 🚀 三步启动项目

### 第一步: 配置阿里云百炼 API Key（可选）

> 如不配置AI功能，项目会使用内置的规则引擎进行数据查询

1. **复制配置文件**
   ```bash
   cp .env.example .env
   ```

2. **获取 API Key**
   - 访问: https://dashscope.console.aliyun.com/
   - 或: https://bailian.console.aliyun.com/
   - 注册/登录阿里云账号
   - 在控制台创建 API-KEY
   - 复制生成的 Key

3. **编辑 `.env` 文件**
   ```
   DASHSCOPE_API_KEY=sk-你的实际key
   PORT=5000
   ```

> **提示**: 也可以直接编辑 `api/.env` 文件配置 API Key

### 第二步: 启动后端服务

```bash
# 进入后端目录
cd api

# 安装 Python 依赖
pip install -r ../requirements.txt

# 初始化数据库（仅首次需要，会生成模拟数据）
python init_db.py

# 启动后端服务
python app.py
```

✅ 后端服务运行在: http://localhost:5000

**验证后端**: 在浏览器访问 http://localhost:5000/
- 应该看到 JSON 格式的服务信息
- `ai_status` 字段会显示是否已配置 API Key

### 第三步: 启动前端服务

```bash
# 在项目根目录
npm install

# 启动开发服务器
npm run client:dev
```

✅ 前端服务运行在: http://localhost:5173

在浏览器中访问 http://localhost:5173 即可看到数据看板！

## 📊 功能说明

### 核心功能
1. **实时数据概览** - 首页展示门诊量、总收入、在院人数、科室数
2. **趋势图表** - 折线图展示门诊量和收入趋势
3. **科室对比** - 柱状图和饼图展示各科室排名
4. **AI 智能问答** - 点击右上角「🤖 AI 助手」按钮，用自然语言查询数据
5. **数据筛选** - 使用顶部日期筛选器按时间范围查询
6. **数据导出** - 支持导出 CSV 格式数据

### AI 问答示例
你可以在 AI 助手中这样提问：
```
查看内科收入趋势
各科室门诊量排名
急诊量统计
科室收入占比
最近一个月的收入走势
```

**有 API Key 时**: 使用通义千问大模型生成智能SQL
**没有 API Key 时**: 使用内置规则引擎解析关键字查询

## 🔧 常见问题

### Q: 前端页面打开但没有数据？
A: 确认后端服务已启动，并且数据库已初始化
   ```bash
   cd api && python init_db.py
   ```

### Q: AI 助手查询结果不够智能？
A: 配置阿里云百炼 API Key 后，会启用真正的大模型进行自然语言理解

### Q: 端口被占用怎么办？
A: 修改 `.env` 文件中的 PORT 配置，或终止占用端口的进程
   ```bash
   lsof -i :5000  # 查看谁占用5000端口
   lsof -i :5173
   ```

### Q: 如何重新生成模拟数据？
A: 删除数据库文件后重新初始化
   ```bash
   rm api/hospital.db  # 或直接删除 hospital.db
   cd api && python init_db.py
   ```

### Q: 如何自定义数据？
A: 修改 `api/init_db.py` 中的模拟数据生成逻辑

## 📁 项目结构

```
/workspace
├── api/                          # Flask 后端
│   ├── app.py                   # 主应用入口
│   ├── database.py              # 数据库配置
│   ├── init_db.py               # 数据库初始化（含模拟数据）
│   ├── .env                     # API Key 配置（新建）
│   ├── routes/                  # API 路由
│   │   ├── dashboard.py         # 看板数据接口
│   │   ├── ai_query.py          # AI 查询接口
│   │   └── export.py            # 数据导出接口
│   └── services/                # 业务逻辑
│       ├── dashboard_service.py # 看板服务
│       ├── bailian_service.py   # 阿里云百炼 AI 服务（核心）
│       └── export_service.py    # 导出服务
├── src/                          # React 前端
│   ├── components/              # 组件
│   │   ├── DashboardCard.tsx    # 数据卡片
│   │   ├── TrendChart.tsx       # 趋势图
│   │   ├── DepartmentChart.tsx  # 科室对比图
│   │   └── AIChat.tsx           # AI 聊天界面
│   ├── lib/api.ts               # API 调用封装（新建）
│   ├── pages/Home.tsx           # 首页
│   └── App.tsx                  # 主应用
├── .env.example                 # 环境变量示例
├── requirements.txt             # Python 依赖
├── package.json                 # Node 依赖
├── vite.config.ts              # Vite 配置（含代理）
└── QUICKSTART.md               # 本文件
```

## 🔌 API 接口说明

### GET /
服务状态检查，返回 AI 配置状态

### GET /api/dashboard
获取看板数据
- 参数: `startDate`, `endDate`, `department` (可选)

### POST /api/ai-query
AI 自然语言查询
- Body: `{"question": "你的问题"}`
- 响应: `{sql, result[], chartType, explanation}`

### GET /api/export
数据导出（CSV格式）
- 参数: `type` (all/outpatient/revenue), `startDate`, `endDate`

## 🎯 下一步建议

1. ✅ 配置阿里云百炼 API Key 启用真正的 AI 智能分析
2. ✅ 修改 `init_db.py` 中的数据逻辑，使用真实的医院运营数据
3. ✅ 扩展数据库表结构，增加更多业务维度（如医生、患者、药品等）
4. ✅ 添加用户登录、权限控制功能
5. ✅ 使用生产级服务器（Gunicorn/Waitress）部署 Flask
6. ✅ 将前端打包后部署到静态服务器或 CDN

## 📞 获取帮助

如遇问题，检查以下内容：
- Python 版本: 3.8 或更高
- Node.js 版本: 16 或更高
- 端口 5000 和 5173 是否被占用
- 数据库文件 hospital.db 是否存在
- 网络是否能正常访问阿里云 API（如使用AI功能）

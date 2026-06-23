# MedDash - 医院运营数据看板

AI辅助编程的医院运营数据看板，使用Trae智能开发平台构建。

## 技术栈

### 前端
- React 18 + TypeScript
- Vite (构建工具)
- Tailwind CSS (样式)
- ECharts (数据可视化)
- React Router (路由)

### 后端
- Python 3 + Flask
- SQLite (数据库)
- Flask-CORS (跨域支持)

## 项目结构

```
/workspace
├── api/                          # Flask 后端
│   ├── app.py                    # 主应用入口
│   ├── database.py               # 数据库配置
│   ├── init_db.py                # 数据库初始化和模拟数据
│   ├── routes/                   # API 路由
│   │   ├── dashboard.py          # 看板数据接口
│   │   ├── ai_query.py           # AI 查询接口
│   │   └── export.py             # 数据导出接口
│   └── services/                 # 业务逻辑
│       ├── dashboard_service.py  # 看板数据服务
│       ├── sql_generator.py      # AI SQL 生成服务
│       └── export_service.py     # 数据导出服务
├── src/                          # React 前端
│   ├── components/               # 组件
│   │   ├── DashboardCard.tsx     # 数据卡片
│   │   ├── TrendChart.tsx        # 趋势图表
│   │   ├── DepartmentChart.tsx   # 科室对比图表
│   │   └── AIChat.tsx            # AI 聊天界面
│   ├── pages/                    # 页面
│   │   └── Home.tsx              # 首页
│   └── App.tsx                   # 应用入口
├── requirements.txt              # Python 依赖
└── package.json                  # Node 依赖
```

## 功能特性

1. **实时数据看板**
   - 今日门诊量、总收入、在院人数等关键指标
   - 趋势图表展示门诊量和收入变化
   - 科室对比柱状图和收入占比饼图

2. **数据筛选**
   - 支持按日期范围筛选数据
   - 灵活的查询条件

3. **AI 智能问答**
   - 自然语言查询医院运营数据
   - 自动生成 SQL 查询
   - 结果可视化展示

4. **数据导出**
   - 支持 CSV 格式导出
   - 可导出门诊量、收入或全部数据

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Node 依赖
npm install
```

### 2. 初始化数据库

```bash
cd api
python init_db.py
```

这将创建 SQLite 数据库并生成模拟数据。

### 3. 启动后端服务

```bash
cd api
python app.py
```

后端服务将在 http://localhost:5000 启动

### 4. 启动前端开发服务器

在另一个终端中：

```bash
npm run dev
```

前端将在 http://localhost:5173 启动

## 使用说明

### 查看看板
- 访问首页查看医院运营数据概览
- 使用顶部导航栏的日期选择器筛选数据范围

### AI 智能查询
- 点击右上角的「AI 助手」按钮
- 在对话框中输入自然语言问题，例如：
  - "查看内科收入趋势"
  - "各科室门诊量对比"
  - "急诊量统计"
- AI 将自动生成 SQL 并展示可视化结果

### 数据导出
- 点击「导出数据」按钮下载 CSV 格式的数据

## 数据库结构

### departments (科室表)
- id: 主键
- name: 科室名称
- description: 科室描述

### outpatients (门诊量表)
- id: 主键
- department_id: 科室 ID
- date: 日期
- count: 门诊量
- emergency_count: 急诊量

### revenues (收入表)
- id: 主键
- department_id: 科室 ID
- date: 日期
- amount: 金额
- type: 收入类型

## API 接口

### GET /api/dashboard
获取看板数据
- 参数: startDate, endDate, department (可选)

### POST /api/ai-query
AI 自然语言查询
- Body: { question: string }

### GET /api/export
导出数据
- 参数: type (all/outpatient/revenue), startDate, endDate

## 开发说明

本项目使用 Trae 智能开发平台辅助开发，展示了 AI 编程在实际项目中的应用。

### 核心技术亮点
- 前后端分离架构
- RESTful API 设计
- 响应式前端界面
- 丰富的数据可视化
- 模拟 AI 自然语言查询功能

## 许可证

MIT License

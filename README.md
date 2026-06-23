<div align="center">

# 🏥 MedDash - AI 辅助医院运营数据看板

**基于大语言模型的智能医院运营决策系统**

[![React](https://img.shields.io/badge/React-18-61dafb?style=for-the-badge&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003b57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![ECharts](https://img.shields.io/badge/ECharts-5-aa4f28?style=for-the-badge&logo=apacheecharts)](https://echarts.apache.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com/)

[功能特性](#-功能特性) · [技术架构](#-技术架构) · [快速开始](#-快速开始) · [部署指南](#-部署指南) · [项目演示](#-项目演示)

</div>

---

## 📋 项目简介

MedDash 是一个 **AI 驱动的医院运营数据看板系统**，结合传统 BI 可视化与大语言模型技术，帮助医院管理者从海量运营数据中快速获取洞察。

通过自然语言交互（如"本周内科收入是否异常？"），系统自动生成 SQL 查询并可视化结果，大幅降低数据分析门槛，提升决策效率。

---

## ✨ 功能特性

### 📊 数据看板
- **核心指标概览**：门诊量、总收入、在院人数等关键指标实时展示
- **趋势分析**：365天历史数据，支持按日期范围筛选
- **科室对比**：12个临床科室的门诊量与收入排行对比
- **收入结构**：挂号费、诊疗费、药费、检查费、手术费等多维度分析

### 🤖 AI 智能问答
- **自然语言查询**：用中文提问，自动生成 SQL 并执行
- **智能图表推荐**：根据查询内容自动选择最佳图表类型
- **规则引擎兜底**：API 不可用时自动切换到本地规则引擎
- **查询解释**：AI 同步生成数据分析结论

### 📁 数据导出
- 支持 CSV / Excel 格式导出
- 按科室、日期范围灵活筛选
- 一键导出完整报表

### 🎨 界面特性
- 现代化深色主题设计
- 响应式布局，支持移动端
- ECharts 高性能图表渲染
- 流畅的交互动画

---

## 🏗️ 技术架构

### 前端技术栈
| 技术 | 用途 |
|------|------|
| **React 18** | UI 框架 |
| **TypeScript** | 类型安全 |
| **Vite** | 构建工具 |
| **Tailwind CSS 3** | 样式框架 |
| **ECharts 5** | 数据可视化 |
| **Zustand** | 状态管理 |
| **React Router** | 路由管理 |

### 后端技术栈
| 技术 | 用途 |
|------|------|
| **Python 3.11** | 运行环境 |
| **Flask** | Web 框架 |
| **SQLite** | 关系数据库 |
| **Flask-CORS** | 跨域支持 |
| **python-dotenv** | 环境变量管理 |
| **DashScope SDK** | 阿里云百炼 API |

### AI 能力
- **阿里云百炼（DashScope）**：大语言模型 API
- **自然语言转 SQL**：Text-to-SQL 能力
- **规则引擎 Fallback**：离线模式保障

---

## 📁 项目结构

```
meddash/
├── api/                          # 后端 Flask 应用
│   ├── app.py                    # 主应用入口
│   ├── database.py               # 数据库连接与初始化
│   ├── init_db.py                # 模拟数据生成脚本
│   ├── routes/                   # API 路由
│   │   ├── dashboard.py          # 看板数据接口
│   │   ├── ai_query.py           # AI 问答接口
│   │   └── export.py             # 数据导出接口
│   └── services/                 # 业务逻辑
│       ├── dashboard_service.py  # 看板数据服务
│       ├── bailian_service.py    # 百炼 AI 服务
│       ├── sql_generator.py      # SQL 生成器
│       └── export_service.py     # 导出服务
├── src/                          # 前端 React 应用
│   ├── components/               # 组件
│   ├── pages/                    # 页面
│   ├── store/                    # 状态管理
│   ├── lib/                      # 工具库
│   └── App.tsx                   # 主应用
├── public/                       # 静态资源
├── render.yaml                   # Render 部署配置
├── railway.json                  # Railway 部署配置
├── vercel.json                   # Vercel 部署配置
└── README.md                     # 项目文档
```

---

## 🚀 快速开始

### 环境要求
- Node.js >= 18
- Python >= 3.10
- npm 或 pnpm

### 1. 克隆项目
```bash
git clone https://github.com/XTB-888/meddash.git
cd meddash
```

### 2. 安装后端依赖
```bash
cd api
pip install -r requirements.txt
```

### 3. 配置 API Key
```bash
# 在 api 目录下创建 .env 文件
echo "DASHSCOPE_API_KEY=your-api-key" > .env
```

> 💡 获取 API Key：[阿里云百炼控制台](https://bailian.console.aliyun.com/)

### 4. 初始化数据库
```bash
python init_db.py
```

### 5. 启动后端服务
```bash
python app.py
# 服务运行在 http://localhost:5000
```

### 6. 安装前端依赖
```bash
cd ..
npm install
```

### 7. 启动前端开发服务器
```bash
npm run dev
# 访问 http://localhost:5173
```

---

## 📊 数据说明

### 模拟数据
项目内置 365 天的医院运营模拟数据，包含：

| 维度 | 详情 |
|------|------|
| **时间范围** | 最近 365 天 |
| **科室数量** | 12 个临床科室 |
| **门诊总量** | 约 66 万+ 人次 |
| **总收入** | 约 1.2 亿元 |
| **收入类型** | 7 种（挂号费、诊疗费、药费、检查费、手术费、住院费、其他） |

### 数据特征
- **季节性波动**：冬季就诊量高（流感季），夏季偏低
- **周末效应**：周末门诊量约为工作日 75%
- **节假日影响**：法定节假日就诊量下降
- **科室差异**：急诊科、外科、内科收入排名前三

---

## 🤖 AI 问答示例

试试这些问题：

| 问题 | 预期效果 |
|------|---------|
| `本月内科收入是多少？` | 自动计算并展示内科月收入 |
| `本周门诊量趋势如何？` | 生成折线图展示最近7天趋势 |
| `哪个科室收入最高？` | 柱状图对比各科室收入 |
| `药费占总收入的比例？` | 饼图展示收入结构 |
| `急诊科日均门诊量？` | 计算并展示急诊科数据 |

---

## ☁️ 部署指南

### 推荐方案：Vercel + PythonAnywhere

#### 前端部署到 Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/XTB-888/meddash)

#### 后端部署到 PythonAnywhere
详细步骤请参考 [DEPLOY_PYTHONANYWHERE.md](./DEPLOY_PYTHONANYWHERE.md)

### 其他方案
- **Railway**：[railway.json](./railway.json) 配置已就绪
- **Render**：[render.yaml](./render.yaml) 配置已就绪（需绑卡）
- **Docker**：可自行构建镜像部署

---

## 🎯 核心亮点

1. **AI + BI 融合**：传统看板 + 自然语言查询，兼顾专业与易用
2. **零配置启动**：内置完整模拟数据，开箱即用
3. **前后端分离**：清晰的 API 边界，便于扩展
4. **多种部署方案**：支持 5+ 种云端部署方式
5. **完整文档**：PRD、架构设计、部署指南一应俱全

---

## 📝 开发说明

本项目使用 **Trae AI 编程助手** 辅助开发，展示了 AI 辅助编程在以下方面的价值：

- ✅ 快速原型开发（从0到1仅需数小时）
- ✅ 自动生成样板代码
- ✅ 智能代码补全与重构
- ✅ Bug 快速定位与修复
- ✅ 文档自动生成

---

## 📄 License

MIT License - 详见 [LICENSE](./LICENSE) 文件

---

<div align="center">

**如果这个项目对你有帮助，欢迎 ⭐ Star 支持！**

 Made with ❤️ by Trae AI

</div>

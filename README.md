# 暖伴 · 智能陪伴机器人

> 用 AI 与物联网技术，为独居老人搭建一座永不打烊的守护桥。

## 项目简介

中国有超过 1.1 亿独居老人，他们面临日常孤独无人陪伴、突发疾病无人发现、紧急情况无法及时求助的困境。暖伴旨在用科技手段解决这些问题。

## 功能特性

### 老人端 App
- **智能对话陪伴** - 基于大语言模型的温暖对话系统
- **用药提醒** - 按时提醒服药，同步通知子女
- **紧急求助** - 语音触发"救命"自动报警
- **视频通话** - 一句话接通子女

### 子女端 App
- **状态查看** - 实时查看老人位置、活动状态
- **异常提醒** - 跌倒检测、用药漏服提醒
- **远程关爱** - 视频通话、发送消息、健康报告
- **数据管理** - 老人健康档案、用药计划

## 技术栈

### 前端
- Vue 3 + TypeScript
- Vite
- Tailwind CSS
- Vue Router 4
- Pinia

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL 8.0
- Redis (可选)

## 项目结构

```
nuanban/
├── nuanban-frontend/      # Vue 前端
├── nuanban-backend/        # Python 后端
├── docs/                   # 项目文档
├── sql/                    # 数据库脚本
└── README.md
```

## 快速开始

### 前端

```bash
cd nuanban-frontend
npm install
npm run dev
```

### 后端

```bash
cd nuanban-backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 数据库

```bash
# 1. 安装 MySQL 8.0
# 2. 创建数据库并执行建表脚本
mysql -u root -p < sql/schema.sql

# 3. （可选）导入测试数据
mysql -u root -p < sql/data.sql
```

## 文档

- [需求分析文档](docs/需求分析文档.md)
- [数据库设计](docs/数据库设计.md)
- [API接口文档](docs/API接口文档.md)

## 开源协议

MIT License

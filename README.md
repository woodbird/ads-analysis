# 广告账户分析平台

基于大模型和agent技术的广告账户分析平台，帮助广告优化师分析广告账户运行情况并提供优化建议。

## 功能特点

- 利用大模型和agent技术分析广告账户数据
- 提供广告优化建议
- 支持多平台广告数据获取（腾讯广告、巨量引擎等）
- Glassmorphism风格的UI设计
- 响应式设计，支持PC和移动端

## 技术架构

- 后端：LangChain + LangGraph实现ReAct模式的AI代理
- 前端：Vite + React实现Glassmorphism风格的UI
- 大模型：OpenAI GPT-4o

## 安装与使用

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 使用示例

用户可以在聊天对话框中询问以下问题：

- 我的广告账户最近7天的表现如何？
- 我的广告投放效果怎么样？
- 有哪些优化建议？
- 我的转化成本是否合理？

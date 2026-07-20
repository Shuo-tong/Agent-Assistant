# 🤖 XiaoAi — 多模态 AI 聊天机器人

基于阿里云 **通义千问（Qwen）** 大模型的轻量级多模态聊天机器人，支持**文字**、**图片**和**语音**对话，提供简洁的 Web 界面和命令行两种交互方式。

---

## ✨ 功能特性

- **多模态输入** — 同一会话中支持文字、图片、音频
- **打字机效果** — AI 响应实时流式输出，带光标动画
- **聊天记录** — 对话持久化存储到 SQLite，自动摘要压缩上下文
- **双模式** — Web 页面（Flask）+ 命令行（CLI）
- **现代化界面** — 暗色主题、响应式设计、简洁美观

---

## 🧰 技术栈

| 层 | 技术 |
|-------|-----------|
| 后端 | Python, Flask, Flask-CORS |
| 前端 | 原生 HTML / CSS / JS |
| LLM API | DashScope（Qwen 3.5 Omni Flash），兼容 OpenAI 协议 |
| 数据库 | SQLite |
| 认证 | API 密钥（`.env` 文件） |

---

## 🚀 快速开始

### 1. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 从 https://dashscope.aliyun.com/ 获取
DASHSCOPE_API_KEY = sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DASHSCOPE_BASE_URL = https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 2. 安装依赖

```bash
pip install openai python-dotenv flask flask-cors
```

> 💡 国内用户推荐使用清华镜像源加速：
> ```bash
> pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple openai python-dotenv flask flask-cors
> ```

### 3. 启动后端

```bash
python AI_api.py
```

服务启动后访问 `http://localhost:5200`。

### 4. 打开聊天页面

在浏览器中打开 **http://localhost:5200/chat**。

---

## 🖥️ 使用方式

### Web 界面

| 操作 | 说明 |
|--------|-----|
| 发送文字 | 输入框中打字，按 `Enter` 发送 |
| 换行 | `Shift + Enter` |
| 上传图片/音频 | 点击 `+` 按钮选择文件 |
| 附带文件发送 | 上传文件后可补充文字说明，然后发送 |

### 命令行模式

```bash
python main.py
```

- 直接输入文字按回车发送
- 用 `@` 前缀发送媒体文件，例如：`@D:/图片/photo.jpg 描述这张图片`
- 输入 `exit` 或 `quit` 退出

---

## 📁 项目结构

```
├── AI_api.py          # Flask API 服务（路由、文件上传、CORS）
├── main.py            # 核心逻辑：LLM 客户端、聊天记录、摘要压缩
├── src/
│   └── ai_chat.html   # Web 前端（单文件 HTML + CSS + JS）
├── .env.example       # 环境变量模板（复制为 .env 并填入密钥）
├── 运行说明.md         # 详细运行说明
└── README.md          # 本文件
```

---

## 🔧 API 接口

| 方法 | 路径 | 说明 |
|--------|------|------|
| `GET` | `/` | 健康检查 |
| `GET` | `/chat` | 聊天页面 |
| `GET` | `/api/chat?content=...` | 纯文本对话 |
| `POST` | `/api/chat` | 多模态对话（文字 + 文件上传） |

---

## 🧠 工作原理

1. **会话管理** — 每个对话属于一个会话（默认 `session_1`），消息存储在 SQLite 数据库中。
2. **上下文压缩** — 当历史消息超过阈值时，自动对较早的对话进行摘要压缩，节省 Token。
3. **多模态支持** — 图片转为 base64 编码，通过兼容 OpenAI 协议的接口发送给 Qwen 模型处理，音频同理。
4. **临时文件** — 上传的文件保存到系统临时目录，处理完成后立即清理。

---

## 📝 许可证

本项目仅供学习和演示用途。

---

> 使用 [DashScope](https://dashscope.aliyun.com/) & [Flask](https://flask.palletsprojects.com/) 构建 ❤️

# 🤖 XiaoAi — Multimodal AI Chatbot

A lightweight, multimodal chatbot powered by Alibaba Cloud's **Qwen (通义千问)** LLM. Supports **text**, **image**, and **audio** conversations through a clean web interface or CLI.

---

## ✨ Features

- **Multimodal Input** — Send text, imagy7ges, or audio files in the same conversation
- **Typing Effect** — AI responses stream in with a live typing cursor
- **Chat History** — Conversations are persisted in SQLite with automatic summarization to stay within context limits
- **Dual Interface** — Web UI (Flask) + CLI mode
- **Modern UI** — Clean, responsive chat interface with dark-header design

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, Flask-CORS |
| Frontend | Vanilla HTML / CSS / JS |
| LLM API | DashScope (Qwen 3.5 Omni Flash) via OpenAI-compatible SDK |
| Database | SQLite |
| Auth | API key via `.env` |

---

## 🚀 Quick Start

### 1. Configure Environment

Copy the `.env` file and fill in your API keys:

```bash
# Get your DashScope API key from: https://dashscope.aliyun.com/
DASHSCOPE_API_KEY = sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DASHSCOPE_BASE_URL = https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 2. Install Dependencies

```bash
pip install openai python-dotenv flask flask-cors
```

> 💡 Use a mirror for faster downloads in China:
> ```bash
> pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple openai python-dotenv flask flask-cors
> ```

### 3. Start the Backend

```bash
python AI_api.py
```

The server starts at `http://localhost:5200`.

### 4. Open the Chat Page

Visit **http://localhost:5200/chat** in your browser.

---

## 🖥️ Usage

### Web Interface

| Action | How |
|--------|-----|
| Send text | Type in the input box and press `Enter` |
| New line | `Shift + Enter` |
| Upload image/audio | Click the `+` button and select a file |
| Send with file | Attach a file, optionally add text, then send |

### CLI Mode

```bash
python main.py
```

- Type your message and press Enter
- Prefix a file path with `@` to send media, e.g. `@D:/images/photo.jpg Describe this image`
- Type `exit` or `quit` to close

---

## 📁 Project Structure

```
├── AI_api.py          # Flask API server (routes, file upload, CORS)
├── main.py            # Core logic: LLM client, chat history, summarization
├── src/
│   └── ai_chat.html   # Web UI (single-file HTML + CSS + JS)
├── .env               # API keys & configuration
├── 运行说明.md         # Chinese setup guide
└── README.md          # This file
```

---

## 🔧 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/chat` | Serve the chat UI |
| `GET` | `/api/chat?content=...` | Text-only chat |
| `POST` | `/api/chat` | Multimodal chat (text + file upload) |

---

## 🧠 How It Works

1. **Session Management** — Each conversation belongs to a session (`session_1` by default). Messages are stored in a SQLite database.
2. **Context Compression** — When history exceeds a threshold, older messages are summarized into a one-line digest to save tokens.
3. **Multimodal Support** — Images are base64-encoded and sent to the Qwen model via OpenAI-compatible API. Audio is handled similarly.
4. **Temporary Files** — Uploaded files are saved to the system temp directory and cleaned up immediately after processing.

---

## 📝 License

This project is for learning and demonstration purposes.

---

> Built with ❤️ using [DashScope](https://dashscope.aliyun.com/) & [Flask](https://flask.palletsprojects.com/)

import os, tempfile, uuid
from flask_cors import CORS
from flask import Flask, jsonify, request, send_from_directory
from main import chat

app = Flask(__name__)
CORS(app)

# 临时文件存在系统临时目录（避免触发 debug reloader & Windows 锁问题）
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "chat_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route('/')
def home():
    return "欢迎访问多模态聊天机器人"

@app.route('/chat')
def chat_page():
    return send_from_directory('src', 'ai_chat.html')

@app.route('/src/<path:filename>')
def src_static(filename):
    return send_from_directory('src', filename)


@app.route('/api/chat', methods=['GET'])
def chat_text():
    """纯文本对话（GET）"""
    content = request.args.get("content", "").strip()
    if not content:
        return jsonify({"error": "缺少 content 参数", "status": 400}), 400

    try:
        reply = chat(content)
        return jsonify({"data": reply, "status": 200})
    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500


@app.route('/api/chat', methods=['POST'])
def chat_multimodal():
    """多模态对话（POST）：支持上传图片/音频 + 可选的文本"""
    content = request.form.get("content", "").strip()
    file = request.files.get("file")

    file_path = None
    try:
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1].lower()
            # 用 uuid 避免文件名冲突，放在系统临时目录
            file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")
            file.save(file_path)

        reply = chat(content, file_path)
        return jsonify({"data": reply, "status": 200})

    except Exception as e:
        return jsonify({"error": str(e), "status": 500}), 500

    finally:
        # 用完删除临时文件
        if file_path and os.path.exists(file_path):
            try:
                os.unlink(file_path)
            except Exception:
                pass  # 如果正在被占用，忽略删除失败


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)


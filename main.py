import os, sys, io, json, base64, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = os.getenv("DASHSCOPE_BASE_URL")

DB = "chat_demo6.db"
SID = "session_1"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}

# ------------------------------------------------
# OpenAI 原生客户端（兼容通义千问 OpenAI 接口）
# ------------------------------------------------
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
mm_client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ------------------------------------------------
# 数据库初始化（兼容原 SQLChatMessageHistory 表结构）
# ------------------------------------------------
conn = sqlite3.connect(DB)
conn.execute("""CREATE TABLE IF NOT EXISTS message_store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    message TEXT NOT NULL
)""")
conn.commit()
conn.close()

# ------------------------------------------------
# 消息辅助函数（保持原样）
# ------------------------------------------------
def msg_content(m):
    d = json.loads(m)
    return d.get("data", {}).get("content", "")

def msg_type(m):
    return json.loads(m).get("type", "?")

def save_message(sid, role, content):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO message_store (session_id, message) VALUES (?, ?)",
        (sid, json.dumps({"type": role, "data": {"content": content}}, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()

# ------------------------------------------------
# 摘要压缩（逻辑完全不变）
# ------------------------------------------------
def build_summary_context(sid):
    conn = sqlite3.connect(DB)
    try:
        rows = conn.execute(
            "SELECT id, message FROM message_store WHERE session_id=? ORDER BY id",
            (sid,),
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []
    conn.close()

    if len(rows) <= 2:
        return None, rows

    old = rows[:-2]
    recent = rows[-2:]
    # 把旧的对话历史浓缩成摘要用的文本片段
    texts = []
    for id, r in old:
        role   = msg_type(r)          # "human" 或 "ai"
        text   = msg_content(r)       # 实际说的话
        brief  = text[:100]            # 太长就截断
        texts.append(f"{role}: {brief}")

    resp = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "把以下对话浓缩成20字内的一句话摘要"},
            {"role": "user", "content": " | ".join(texts)},
        ],
    )
    summary = resp.choices[0].message.content
    print(f"  摘要: {summary}")
    return summary, recent

# ------------------------------------------------
# 文件 / 媒体 辅助函数
# ------------------------------------------------
def file_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def build_multimodal_message(text, image_path):
    """构建图文消息（OpenAI 原生格式）"""
    b64_data = file_to_b64(image_path)
    ext = os.path.splitext(image_path)[1].lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp",
            ".bmp": "image/bmp", ".gif": "image/gif"}.get(ext, "image/jpeg")
    return [
        {"type": "text", "text": text},
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64_data}"}},
    ]

# ------------------------------------------------
# 核心对话函数
# ------------------------------------------------
def chat(user_msg, media_file=None):
    """单次对话：处理文字 / 图片，返回回复文本"""
    if not user_msg.strip() and not media_file:
        return ""

    final_text = user_msg
    is_image = False

    if media_file:
        is_image = True
        if not user_msg.strip():
            final_text = "请分析这张图片"

    # 构建带摘要的上下文
    summary, recent_rows = build_summary_context(SID)
    messages = [{"role": "system", "content": "你叫小爱，简洁友好地回答"}]
    if summary:
        messages.append({"role": "system", "content": f"[历史摘要] {summary}"})
    for _, rmsg in recent_rows:
        t, c = msg_type(rmsg), msg_content(rmsg)
        if t == "human":
            messages.append({"role": "user", "content": c})
        elif t == "ai":
            messages.append({"role": "assistant", "content": c})

    # 调用 LLM
    if is_image:
        messages.append({"role": "user", "content": build_multimodal_message(final_text, media_file)})
    else:
        messages.append({"role": "user", "content": final_text})
        # reply = ""
        # stream = client.chat.completions.create(
        #     model="qwen-plus",
        #     messages=messages,
        #     # stream=True,
        # )
        # for chunk in stream:
        #     if chunk.choices[0].delta.content:
        #         reply += chunk.choices[0].delta.content
    response = mm_client.chat.completions.create(
        model="qwen3.5-omni-flash",
        messages=messages,
    )
    reply = response.choices[0].message.content
    # 保存历史
    save_message(SID, "human", final_text)
    save_message(SID, "ai", reply)
    return reply


if __name__ == "__main__":
    # 简单 CLI 交互，替代 Gradio
    print("🤖 小爱聊天机器人（输入 exit 退出）")
    print("   上传图片路径以 @ 开头，如 @D:/path/to/image.jpg\n")
    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        media_file = None
        if user_input.startswith("@"):
            parts = user_input.split(maxsplit=1)
            media_file = parts[0][1:]
            user_input = parts[1] if len(parts) > 1 else ""

        reply = chat(user_input, media_file)
        print(f"\n小爱: {reply}")

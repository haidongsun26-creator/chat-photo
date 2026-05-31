# -*- coding: utf-8 -*-
"""chat-photo 网页版后端 —— 零第三方依赖（仅 Python 标准库）。

职责：
  - 静态托管 public/ 下的前端
  - POST /api/extract：收聊天截图 → 用 urllib 直调 Claude Messages API 看图 → 返回结构化对话 JSON

运行：
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 server/app.py            # 默认 http://127.0.0.1:8000
依赖：无（http.server / json / urllib / base64 全是标准库）
"""
import os
import re
import json
import base64
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from extract_prompt import SYSTEM_PROMPT

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("CHAT_PHOTO_MODEL", "claude-opus-4-8")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PORT = int(os.environ.get("PORT", "8000"))

MIME = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".png": "image/png", ".svg": "image/svg+xml",
        ".json": "application/json; charset=utf-8"}


def call_claude(image_b64: str, media_type: str, hint: str) -> dict:
    """调 Claude 看图，返回解析后的对话 dict。失败抛异常。"""
    if not API_KEY:
        raise RuntimeError("未设置 ANTHROPIC_API_KEY，请在环境变量或 .env 里配置后重启。")
    user_text = "请提取这张聊天截图的对话。"
    if hint:
        user_text += f" 补充背景：{hint}"
    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64",
                                             "media_type": media_type, "data": image_b64}},
                {"type": "text", "text": user_text},
            ],
        }],
    }
    req = urllib.request.Request(
        API_URL, data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json", "x-api-key": API_KEY,
                 "anthropic-version": "2023-06-01"},
        method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    # 容错：模型偶尔包了 ```json 代码块或前后有解释，抠出最外层 {}
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise RuntimeError("Claude 未返回可解析的 JSON：" + text[:200])
    return json.loads(m.group(0))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("content-type", ctype)
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # 静音默认访问日志
        pass

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            path = "/index.html"
        target = (PUBLIC / path.lstrip("/")).resolve()
        if PUBLIC not in target.parents and target != PUBLIC or not target.is_file():
            return self._send(404, {"error": "not found"})
        ctype = MIME.get(target.suffix, "application/octet-stream")
        self._send(200, target.read_bytes(), ctype)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/extract":
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("content-length", "0"))
            body = json.loads(self.rfile.read(n).decode("utf-8"))
            image = body.get("image", "")
            hint = body.get("hint", "")
            # 前端传 dataURL：data:image/png;base64,xxxx
            mt, b64 = "image/png", image
            m = re.match(r"data:(image/[\w.+-]+);base64,(.*)", image, re.S)
            if m:
                mt, b64 = m.group(1), m.group(2)
            if not b64:
                return self._send(400, {"error": "缺少图片"})
            result = call_claude(b64, mt, hint)
            self._send(200, result)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:300]
            self._send(502, {"error": f"Claude API 错误 {e.code}", "detail": detail})
        except Exception as e:  # noqa
            self._send(500, {"error": str(e)})


if __name__ == "__main__":
    key_state = "已配置" if API_KEY else "⚠️ 未配置（看图会失败，请设 ANTHROPIC_API_KEY）"
    print(f"chat-photo web 运行中：http://127.0.0.1:{PORT}")
    print(f"模型：{MODEL}    API Key：{key_state}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()

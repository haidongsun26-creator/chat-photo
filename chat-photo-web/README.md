# chat-photo web

把聊天对话做成卡通对话漫画的网页版。**手动输入**模式纯静态零依赖、双击即用；另可选启用本地后端，**上传聊天截图自动提对话**。

## 怎么用

直接用浏览器打开 `public/index.html` 即可（无需联网、无需安装任何东西）：

1. 填标题
2. 逐条输入对话，每句选「对方/自己」+ 表情（或见下方「上传截图自动提对话」）
3. 选风格（粉色糖果 / 冷调清新 / 暗黑潮酷 / 暖黄复古）
4. 点「生成 / 刷新预览」，再点「导出 PNG」

也可以丢到任意静态托管（GitHub Pages / Netlify / Vercel 静态）分享给别人用。

## 上传聊天截图，自动提对话

页面第 2 步有「点此选图 / 拖入聊天截图」上传区：选图（支持多张）后会自动识别对话、灌进下方编辑器并出预览，可再手动微调。

此功能需要本地后端 + Claude API Key：

```bash
cp .env.example .env       # 填 ANTHROPIC_API_KEY
./run.sh                   # http://127.0.0.1:8000，从这里打开网页
```

看图规则与 skill 同源（写在 `server/extract_prompt.py`）：绿色=自己/白色=对方、语音转文字归发送方、忽略语音时长与时间戳。
**纯静态直接打开**（不经 `./run.sh`）时，上传区会提示连不上后端，此时改用手动输入即可——出图功能完全不受影响。

## 两种用法，按需选

- **手动输入**：零 key、零后端，双击 `public/index.html` 即用，排版出图全在前端（复用 skill 的视觉，`html-to-image` 导出 PNG）。
- **上传截图自动提对话**：需 Claude API key + 启动本地后端（见上一节），看图识别省去手敲对话。

两者出图环节完全一致，区别只在「对话从哪来」。

## 文件

| 文件 | 作用 |
|---|---|
| `public/index.html` | 对话编辑器 + 选风格 + 预览 + 导出（主入口） |
| `public/render.js` | 对话数据 → 分镜 DOM → `html-to-image` 导出 PNG |
| `public/themes.css` | 4 套风格变量（抽自 skill `template.html`） |
| `public/comic.css` | 矢量兔角色 + 全套表情态（含 .shy/.angry/.sad/.tear/.shock） |
| `server/app.py` | 可选后端：静态托管 + `POST /api/extract`（上传截图 → 调 Claude 看图 → 返回对话 JSON），Python 标准库零依赖 |
| `server/extract_prompt.py` | 看图提对话的系统提示词，规则与 skill 同源 |

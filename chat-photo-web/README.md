# chat-photo web

把聊天对话做成卡通对话漫画的网页版。**纯静态、零依赖、零 key、零后端** —— 双击即用。

## 怎么用

直接用浏览器打开 `public/index.html` 即可（无需联网、无需安装任何东西）：

1. 填标题
2. 逐条输入对话，每句选「对方/自己」+ 表情
3. 选风格（粉色糖果 / 冷调清新 / 暗黑潮酷 / 暖黄复古）
4. 点「生成 / 刷新预览」，再点「导出 PNG」

也可以丢到任意静态托管（GitHub Pages / Netlify / Vercel 静态）分享给别人用。

## 为什么是手动输入对话

「看图自动提对话」需要多模态模型（Claude/OpenAI/Gemini），而它们都要付费 API key。
在无 key 的前提下，去掉看图环节、改为手动输入，是唯一能**零成本、立即可用**的方案。
排版与出图本就在前端完成（复用 skill 的视觉，`html-to-image` 导出 PNG），所以整个网页彻底不需要后端。

## 文件

| 文件 | 作用 |
|---|---|
| `public/index.html` | 对话编辑器 + 选风格 + 预览 + 导出（主入口） |
| `public/render.js` | 对话数据 → 分镜 DOM → `html-to-image` 导出 PNG |
| `public/themes.css` | 4 套风格变量（抽自 skill `template.html`） |
| `public/comic.css` | 矢量兔角色 + 全套表情态（含 .shy/.angry/.sad/.tear/.shock） |
| `server/` | **可选**。若将来拿到 Claude key，可启用它做「上传截图自动提对话」 |

## 可选：将来有 key 时启用「看图自动提对话」

`server/app.py`（Python 标准库，零第三方依赖）已写好：上传截图 → 调 Claude 看图 → 返回对话 JSON。
有 key 时：
```bash
cp .env.example .env       # 填 ANTHROPIC_API_KEY
./run.sh                   # http://127.0.0.1:8000
```
看图规则与 skill 同源（写在 `server/extract_prompt.py`）：绿色=自己/白色=对方、语音转文字归发送方、忽略语音时长与时间戳。
当前无 key，此后端不启用，不影响纯静态页使用。

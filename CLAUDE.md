# CLAUDE.md

本文件给 Claude Code 提供本仓库的定位与约定。

## 仓库定位

把**聊天对话生成卡通对话漫画 PNG**。两条交付线，共享同一套视觉规范（粗黑描边 + 扁平填色的矢量小兔，4 种风格）：

1. **chat-photo Skill**（`.claude/skills/chat-photo/`）——在 Claude Code 内：看聊天截图 → 提对话 → 渲染多格漫画。
2. **网页版**（`chat-photo-web/`）——纯本地网页：手动输入对话 → 出图。

## 目录约定

```
.claude/skills/chat-photo/   # Skill 本体
  SKILL.md                   # 触发、流程、提对话规则、风格表、视觉规范
  template.html              # 漫画模板（4 主题 + 矢量角色 + 表情态）
  examples/                  # 示例（quarrel-makeup 情侣吵架又和好）
chat-photo-web/              # 网页版
  public/index.html          # 对话编辑器 + 选风格 + 预览 + 导出（主入口，纯静态）
  public/render.js           # 对话数据 → 分镜 DOM → html-to-image 导出 PNG
  public/themes.css          # 4 套风格变量（与 skill 同源）
  public/comic.css           # 矢量兔角色 + 全套表情态
  server/                    # 可选 Python 后端（有 key 时启用「看图自动提对话」）
comic.html / comic.png       # 最近一次手工生成的漫画与源码
seedream_mcp/                # 第三方文生图 MCP（clone，未启用，已 gitignore）
```

## 核心规则（提对话，三条硬约束）

1. **气泡颜色定身份，颜色优先于位置**：绿色=自己、白色/灰色=对方。
2. **语音转文字白框归语音发送方**：语音气泡下方白框是转文字结果，归发送方。
3. **只取聊天文本**：语音时长、时间戳、已读/撤回/拍一拍等元信息一律忽略，不进漫画。

权威定义在 `.claude/skills/chat-photo/SKILL.md`，改规则以它为准。

## 常用命令

```bash
# 渲染 HTML → PNG（Skill 出图用）
export PATH="$PATH:$HOME/Library/Python/3.9/bin"
shot-scraper comic.html --width 1080 --height 1350 --retina --wait 1500 -o comic.png

# 网页版：浏览器直接打开（纯静态，无需服务）
open chat-photo-web/public/index.html

# 网页版可选后端（需 Claude key，看图自动提对话）
cd chat-photo-web && cp .env.example .env   # 填 ANTHROPIC_API_KEY
./run.sh                                     # http://127.0.0.1:8000
```

## 视觉规范

画布 1080×1350；角色粗黑描边 `4~5px`、扁平填色、圆头长耳大眼+腮红+手脚；表情态 `.shy/.angry/.sad/.tear/.shock`；气泡白底粗描边、朝说话角色出三角；字体 Noto Sans SC。改样式时 skill 的 `template.html` 与网页的 `comic.css` 要同步。

## 环境备注

- 本机**无 Node/npm/brew**；Python 3.9 可用。网页后端因此用 Python 标准库实现（零第三方依赖）。
- 出图依赖 `shot-scraper`（`~/Library/Python/3.9/bin/`）+ `playwright==1.47.0`。
- 采用 MIT 许可证（见 `LICENSE`）。

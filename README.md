# chat-photo

把**聊天对话变成卡通对话漫画 PNG** 的工具集。两种用法：一个可在 Claude Code 里调用的 Skill，一个纯本地运行的网页版。

视觉风格统一为「粗黑描边 + 扁平填色」的圆润小动物（红兔 / 绿兔），支持 4 种配色风格，直接可发小红书。

## 包含什么

| 部分 | 位置 | 说明 |
|---|---|---|
| **chat-photo Skill** | `.claude/skills/chat-photo/` | Claude Code 技能：看聊天截图 → 自动提对话 → 渲染多格对话漫画 PNG |
| **网页版** | `chat-photo-web/` | 纯静态网页：手动输入对话 → 选风格 → 预览 → 导出 PNG（零依赖、零 key） |
| **示例成图** | `comic.png`、`示例-对话漫画.png` | 历史生成的漫画样张 |

## 安装 / 使用

### 网页版（推荐，最简单）

无需安装任何东西，浏览器直接打开：

```
chat-photo-web/public/index.html
```

逐条输入对话 → 每句选「对方/自己」+ 表情 → 选风格 → 点「生成 / 刷新预览」→「导出 PNG」。
全程在浏览器本地完成，不上传数据、不需要联网账号。

### chat-photo Skill（在 Claude Code 里）

在 Claude Code 中说 `/chat-photo`，或「把这张聊天截图做成漫画」，然后拖入聊天截图。
依赖 `shot-scraper`（HTML→PNG 渲染）：

```bash
export PATH="$PATH:$HOME/Library/Python/3.9/bin"
# shot-scraper 报 devtools 错时：pip3 install 'playwright==1.47.0' && shot-scraper install
```

## 使用方式说明

- **气泡身份**：绿色气泡 = 自己（右），白色 / 灰色 = 对方（左）；颜色优先于左右位置。
- **窗格数**：按对话信息量自动决定（≤4 句→4 格，≤6→6 格，否则 9 格）。
- **风格**：粉色糖果 / 冷调清新 / 暗黑潮酷 / 暖黄复古，一键切换。
- **看图自动提对话**（网页版可选）：需 Claude API key，配置见 `chat-photo-web/README.md`；当前无 key，网页走手动输入。

## 备注

- `seedream_mcp/` 是 clone 来的第三方文生图 MCP（备用，当前未启用），不纳入本仓库。

## License

[MIT](LICENSE) © 2026 Playboydgs

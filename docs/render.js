// chat-photo 前端渲染：对话 JSON → 分镜 DOM → html-to-image 导出 PNG
// 与 skill 同源：复用 comic.css 的矢量角色 + 表情态。

const EMOJI = { happy:"😄", shy:"💗", angry:"💢", sad:"💧", shock:"❗", sleepy:"😴", normal:"✨" };
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;" }[c]));

// 一只矢量兔（color: 'red'|'green'，emotion 决定表情 class，right 决定靠右）
function roleHTML(color, emotion, right) {
  const cls = ["role", color, right ? "right" : "", emotion || "normal"].filter(Boolean).join(" ");
  const tears = emotion === "sad" ? '<span class="tear l"></span><span class="tear r"></span>' : "";
  const armUp = (emotion === "shy" || emotion === "shock") ? "up " : "";
  return `<div class="${cls}">
    <div class="ear l"><span class="ear-in"></span></div>
    <div class="ear r"><span class="ear-in"></span></div>
    <div class="head">
      <span class="eye l"><span class="spark"></span></span>
      <span class="eye r"><span class="spark"></span></span>
      ${tears}
      <span class="nose"></span><span class="mouth"></span>
      <span class="blush l"></span><span class="blush r"></span>
    </div>
    <div class="arm ${armUp}l"></div><div class="arm ${armUp}r"></div>
    <div class="cbody"></div>
    <div class="foot l"></div><div class="foot r"></div>
  </div>`;
}

function cellHTML(line, idx) {
  const side = line.side === "r" ? "r" : "l";       // 气泡侧
  const right = side === "r";                         // 角色靠右
  const color = line.color || (right ? "green" : "red");
  const deco = EMOJI[line.emotion] || EMOJI.normal;
  const decoPos = right ? "top:22px;left:34px" : "top:22px;right:34px";
  return `<div class="cell">
    <span class="panel-no">${idx + 1}</span>
    <div class="bubble ${side}">${esc(line.text).replace(/\n/g, "<br>")}</div>
    ${roleHTML(color, line.emotion, right)}
    <span class="deco" style="${decoPos}">${deco}</span>
  </div>`;
}

// data: {title,subtitle,panels,lines[]}，theme: 'theme-candy' 等
function renderComic(data, theme) {
  const n = data.lines.length;
  const gridClass = n <= 4 ? "g4" : n <= 6 ? "g6" : "g9";
  const cells = data.lines.map(cellHTML).join("\n");
  return `<div class="stage ${theme}">
    <div class="title">${esc(data.title || "对话漫画")}</div>
    <div class="subtitle">${esc(data.subtitle || "")}</div>
    <div class="grid ${gridClass}">${cells}</div>
  </div>`;
}

// 导出当前 .stage 为 PNG（2× 高清）
async function exportPNG(stageEl, filename) {
  const dataUrl = await htmlToImage.toPng(stageEl, {
    pixelRatio: 2, width: 1080, height: 1350,
    style: { transform: "none" }, cacheBust: true,
  });
  const a = document.createElement("a");
  a.href = dataUrl; a.download = filename || "chat-photo.png";
  a.click();
}

window.ChatPhoto = { renderComic, exportPNG };

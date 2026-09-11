import os

with open('code_body.html', 'r', encoding='utf-8') as f:
    code_html = f.read()

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>3D 粒子玫瑰 · 本地全屏极客盛宴</title>
<style>
:root {
  color-scheme: dark;
  --bg: #020403;
  --panel-bg: rgba(6, 9, 14, 0.75);
  --accent: #ff2d55;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  width: 100vw; height: 100vh; overflow: hidden;
  background: var(--bg); color: #dddbd8; user-select: none;
}

#app-container {
  position: absolute; inset: 0; width: 100%; height: 100%; display: flex;
}

/* 左侧代码编辑器面板 */
#code-panel {
  position: absolute; top: 0; left: 0; height: 100%;
  width: 440px; max-width: 46vw; z-index: 10;
  display: flex; flex-direction: column;
  background: var(--panel-bg);
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 15px 0 45px rgba(0, 0, 0, 0.6);
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
  pointer-events: auto;
}

#code-panel.collapsed {
  transform: translateX(-100%);
  opacity: 0;
  pointer-events: none;
}

/* macOS 风格窗口与标签栏 */
.editor-header {
  height: 42px; background: rgba(9, 13, 20, 0.85);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  display: flex; align-items: center; padding: 0 16px; gap: 10px;
  flex-shrink: 0;
}
.window-dots { display: flex; gap: 7px; }
.dot { width: 11px; height: 11px; border-radius: 50%; }
.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }

.editor-tab {
  margin-left: 8px; display: flex; align-items: center; gap: 6px;
  color: #c9d1d9; font-size: 12px; font-family: "Menlo", "Consolas", monospace;
}
.scroll-status {
  margin-left: auto; font-size: 11px; color: #58a6ff;
  display: flex; align-items: center; gap: 5px; cursor: pointer;
  padding: 3px 8px; border-radius: 12px; background: rgba(88, 166, 255, 0.12);
  transition: all 0.2s;
}
.scroll-status:hover { background: rgba(88, 166, 255, 0.25); }

/* 代码滚动视口 */
.code-viewport {
  flex: 1; overflow: hidden; position: relative;
  font-family: "JetBrains Mono", "Fira Code", "Menlo", "Consolas", monospace;
  font-size: 11.8px; line-height: 22px;
}
.code-scroll-content {
  position: absolute; top: 0; left: 0; width: 100%;
  will-change: transform;
}

/* 代码行 */
.line {
  display: flex; width: 100%; height: 22px; line-height: 22px;
  white-space: pre;
}
.ln {
  width: 48px; padding-right: 14px; text-align: right;
  color: #38495f; user-select: none; flex-shrink: 0;
  border-right: 1px solid rgba(255, 255, 255, 0.04);
}
.cl {
  padding-left: 14px; color: #c9d1d9; overflow: hidden;
  text-overflow: ellipsis;
}

/* 语法高亮配色 (One Dark / VS Code) */
.kw   { color: #ff5370; font-weight: 600; } /* def, class, import */
.fn   { color: #61afef; }                   /* 函数 */
.cls  { color: #e5c07b; font-weight: 600; } /* 类 */
.str  { color: #98c379; }                   /* 字符串 */
.num  { color: #d19a66; }                   /* 数字 */
.cm   { color: #6272a4; font-style: italic; } /* 注释 */
.bi   { color: #f1fa8c; }                   /* 内置函数 */
.self { color: #ff79c6; }                   /* self */
.op   { color: #56b6c2; }                   /* 运算符 */
.punc { color: #7f848e; }                   /* 标点 */
.var  { color: #abb2bf; }                   /* 变量 */

/* 3D 舞台 */
#stage {
  position: absolute; inset: 0; width: 100%; height: 100%;
}
canvas { display: block; width: 100%; height: 100%; }

/* 悬浮提示与控制面板 */
#hint {
  position: fixed; top: 22px; left: 470px; font-size: 11px;
  letter-spacing: .12em; color: #999890; transition: opacity .5s, left .4s;
  pointer-events: none; z-index: 20;
}
#code-panel.collapsed ~ #hint { left: 25px; }
#hint small { display: block; font-size: 10px; letter-spacing: .03em; color: #636962; margin-top: 5px; }

#ui {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 6px; align-items: center; padding: 8px 14px;
  background: rgba(13, 17, 23, 0.85); border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 30px; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.6); transition: opacity .5s;
  white-space: nowrap; z-index: 30;
}
body.quiet #ui, body.quiet #hint, body.quiet #settings { opacity: 0; pointer-events: none; }
button {
  background: transparent; border: 0; color: #ddd; padding: 7px 13px;
  cursor: pointer; border-radius: 20px; font: inherit; font-size: 12px;
  transition: all .2s; display: flex; align-items: center; gap: 5px;
}
button:hover, button.active { background: #34322f; color: white; }
button.primary { background: #ff2d55; color: white; box-shadow: 0 0 12px rgba(255, 45, 85, 0.5); }

#settings {
  display: none; position: fixed; bottom: 82px; left: 50%; transform: translateX(-50%);
  padding: 18px 22px; width: 310px; border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px; background: rgba(11, 16, 14, 0.94);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  z-index: 30;
}
#settings label { display: grid; grid-template-columns: 75px 1fr 36px; gap: 8px; margin: 10px 0; align-items: center; color: #b9beb7; font-size: 12px; }
input { accent-color: #ff2d55; width: 100%; cursor: pointer; }
output { text-align: right; font-size: 11px; color: #aeb7ac; }
#error { display: none; position: absolute; inset: 35% 10%; font-size: 16px; text-align: center; line-height: 2; color: #ff5252; }
</style>
</head>
<body>
<div id="app-container">
  <!-- 左侧代码编辑器视图 (自动滚动展示原版 Python 源码) -->
  <aside id="code-panel">
    <div class="editor-header">
      <div class="window-dots">
        <div class="dot red"></div>
        <div class="dot yellow"></div>
        <div class="dot green"></div>
      </div>
      <div class="editor-tab">
        <span>🐍</span> particle_rose_3d.py
      </div>
      <div class="scroll-status" id="scroll-toggle" title="点击或按 S 键暂停/恢复滚动">
        <span id="scroll-icon">▶</span> <span id="scroll-text">滚动中</span>
      </div>
    </div>
    <div class="code-viewport" id="code-viewport">
      <div class="code-scroll-content" id="code-scroll-content">
__CODE_BODY__
      </div>
    </div>
  </aside>

  <!-- 3D 粒子玫瑰舞台 (完全运行您提供的 WebGL 2 引擎) -->
  <main id="stage">
    <canvas id="canvas" aria-label="三维粒子玫瑰动画"></canvas>
    <div id="error"></div>
  </main>

  <div id="hint">
    PARTICLE ROSE · NATIVE FULLSCREEN
    <small>3D 全息线框 · 原版代码自动滚动 · 拖动旋转 · 滚轮缩放</small>
  </div>

  <div id="ui">
    <button id="fullscreen-btn" class="primary">⛶ 全屏模式</button>
    <button id="play">暂停</button>
    <button id="spin" class="active">自动旋转</button>
    <button id="box" class="active">3D线框</button>
    <button id="code-btn" class="active">源码面板</button>
    <button id="options">视觉参数</button>
    <button id="snapshot">保存画面</button>
    <button id="reset">视口复位</button>
  </div>

  <div id="settings">
    <label>播放速度<input id="speed" type="range" min="0" max="2" step="0.05" value="1"><output>1.00</output></label>
    <label>粒子流动<input id="flow" type="range" min="0" max="2" step="0.05" value="1"><output>1.00</output></label>
    <label>柔光辉光<input id="bloom" type="range" min="0" max="1.8" step="0.05" value="0.85"><output>0.85</output></label>
    <label>画面亮度<input id="exposure" type="range" min="0.5" max="2.2" step="0.05" value="1.3"><output>1.30</output></label>
    <label>代码滚速<input id="scroll-speed" type="range" min="0.2" max="3.0" step="0.1" value="1.0"><output>1.00</output></label>
  </div>
</div>

<script>
'use strict';
// ==================== 1. 原版 Python 源码自动平滑滚动系统 ====================
const codeViewport = document.getElementById('code-viewport');
const codeContent = document.getElementById('code-scroll-content');
let scrollPos = 0;
let scrollSpeed = 0.6; // 像素/帧
let isAutoScroll = true;
let isHovered = false;

// 复制一份内容实现无缝平滑无限循环滚动
const originalHtml = codeContent.innerHTML;
codeContent.innerHTML += originalHtml;

function updateAutoScroll() {
  if (isAutoScroll && !isHovered) {
    scrollPos += scrollSpeed;
    const halfHeight = codeContent.scrollHeight / 2;
    if (scrollPos >= halfHeight) {
      scrollPos -= halfHeight;
    }
    codeContent.style.transform = `translate3d(0, -${scrollPos}px, 0)`;
  }
  requestAnimationFrame(updateAutoScroll);
}
requestAnimationFrame(updateAutoScroll);

codeViewport.addEventListener('mouseenter', () => { isHovered = true; });
codeViewport.addEventListener('mouseleave', () => { isHovered = false; });
codeViewport.addEventListener('wheel', (e) => {
  scrollPos += e.deltaY;
  const halfHeight = codeContent.scrollHeight / 2;
  if (scrollPos < 0) scrollPos += halfHeight;
  if (scrollPos >= halfHeight) scrollPos -= halfHeight;
  codeContent.style.transform = `translate3d(0, -${scrollPos}px, 0)`;
  e.preventDefault();
}, { passive: false });

function toggleScrollState() {
  isAutoScroll = !isAutoScroll;
  document.getElementById('scroll-icon').textContent = isAutoScroll ? '▶' : '⏸';
  document.getElementById('scroll-text').textContent = isAutoScroll ? '滚动中' : '已暂停';
}
document.getElementById('scroll-toggle').onclick = toggleScrollState;

// ==================== 2. 用户指定 WebGL 2 粒子玫瑰与 3D 线框引擎 ====================
const TAU = Math.PI * 2;
const PARAMS = {
  speed: 1, flow: 1, bloom: 0.85, exposure: 1.3, spin: true, box: true, paused: false,
  duration: 16, cameraDistance: 8.0, cameraPitch: 0.13, manualYaw: 0, manualPitch: 0,
  codeVisible: true
};

const canvas = document.getElementById('canvas');
const gl = canvas.getContext('webgl2', {
  alpha: false, antialias: false, preserveDrawingBuffer: true, depth: false
});

if (!gl) {
  document.getElementById('error').style.display = 'block';
  document.getElementById('error').textContent = '此动画需要支持 WebGL 2 的环境，请启用图形硬件加速。';
  throw new Error('WebGL 2 unavailable');
}

const HDR = !!gl.getExtension('EXT_color_buffer_float');
gl.getExtension('OES_texture_float_linear');

let rng = 932751;
function rand() {
  rng = (Math.imul(rng, 1664525) + 1013904223) >>> 0;
  return rng / 4294967296;
}
function gaussian() {
  return Math.sqrt(-2 * Math.log(Math.max(1e-8, rand()))) * Math.cos(TAU * rand());
}
const mix = (a, b, t) => a + (b - a) * t;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
function smooth(a, b, x) {
  let k = clamp((x - a) / (b - a));
  return k * k * (3 - 2 * k);
}
function normalize(v) {
  let m = Math.hypot(...v);
  return v.map(x => x / m);
}

const particles = [], threads = [];
function vertex(dst, p, c, opacity, size, flow, seed) {
  dst.push(p[0], p[1], p[2], c[0], c[1], c[2], opacity, size, flow, seed);
}
function addParticle(p, c, a = 0.45, size = 1.05, flow = 1, seed = rand() * 100) {
  vertex(particles, p, c, a, size, flow, seed);
}
function addThread(p, q, c, a = 0.09, flow = 1, seed = 0) {
  vertex(threads, p, c, a, 1, flow, seed);
  vertex(threads, q, c, a, 1, flow, seed);
}

const ivory = [1, 0.93, 0.87], pink = [1, 0.46, 0.48], coral = [1, 0.13, 0.15], darkred = [0.53, 0.04, 0.055];
const lerpc = (a, b, t) => a.map((v, i) => mix(v, b[i], t));

function flowerTransform(p, b) {
  const cp = Math.cos(b.az), sp = Math.sin(b.az), ct = Math.cos(b.tilt), st = Math.sin(b.tilt);
  return [
    b.x + b.scale * (p[0] * cp + p[1] * sp * st + p[2] * sp * ct),
    b.y + b.scale * (p[1] * ct - p[2] * st),
    b.z + b.scale * (-p[0] * sp + p[1] * cp * st + p[2] * cp * ct)
  ];
}

const blooms = [{ x: 0, y: 1.05, z: 0, scale: 0.78, tilt: 0, az: 0, phase: 0.2 }];
for (let j = 0; j < 4; j++) {
  let a = j * TAU / 4 + 0.35;
  blooms.push({ x: 0.49 * Math.sin(a), y: 0.75 + 0.05 * Math.sin(a * 2), z: 0.49 * Math.cos(a), scale: 0.76, tilt: 0.65, az: a, phase: rand() * TAU });
}
for (let j = 0; j < 6; j++) {
  let a = j * TAU / 6 + 0.11;
  blooms.push({ x: 0.72 * Math.sin(a), y: 0.22 + 0.09 * Math.cos(a * 3), z: 0.72 * Math.cos(a), scale: 0.72, tilt: 1.02, az: a, phase: rand() * TAU });
}

const petalCounts = [3, 5, 7, 8, 9];
function petalPoint(layer, j, u, v, phase) {
  const n = petalCounts[layer], k = layer / 4, a = j * TAU / n + phase + layer * 0.58;
  const spread = (TAU / n) * (0.67 + 0.08 * k);
  const w = Math.sin(Math.PI * v / 2);
  const tip = 0.105 + k * 0.81;
  let r = 0.027 + k * 0.015 + (tip - 0.025) * Math.pow(w, 1.02);
  let angle = a + u * spread * (0.52 + 0.48 * w);
  let y = -0.33 + (0.96 - 0.08 * k) * Math.pow(v, 0.76) - (0.018 + 0.06 * k) * Math.pow(v, 5);
  y += 0.065 * u * u * Math.pow(v, 1.6) + 0.025 * Math.sin(u * 4.5 + j * 1.7 + phase) * v * v;
  const edge = Math.pow(v, 4);
  r += 0.03 * edge * Math.sin(u * 9 + phase + j * 1.2) + 0.02 * Math.sin(v * 6 + u * 5 + j) * v;
  y += 0.035 * edge * Math.sin(u * 10.5 + j + phase);
  r += 0.037 * k * smooth(0.75, 1, v);
  return [Math.sin(angle) * r, y, Math.cos(angle) * r];
}

function petalColour(layer, j, u, v, b) {
  let rim = Math.max(smooth(0.82, 1, v) * 0.97, smooth(0.85, 1, Math.abs(u)) * 0.95);
  let patch = 0.5 + 0.5 * Math.sin(u * 4.5 + v * 5.2 + j * 1.39 + b.phase);
  let c = lerpc(coral, pink, 0.08 + 0.10 * patch);
  c = lerpc(c, ivory, clamp(rim + 0.08 * patch));
  let light = 0.68 + 0.25 * smooth(0.08, 0.75, v) + 0.07 * patch;
  if (v < 0.2) c = lerpc([0.30, 0.21, 0.105], c, smooth(0, 0.22, v));
  return c.map(z => z * light);
}

const anchors = [];
for (const b of blooms) {
  for (let layer = 0; layer < 5; layer++) {
    for (let j = 0; j < petalCounts[layer]; j++) {
      const count = 350 + layer * 28;
      for (let k = 0; k < count; k++) {
        let u = rand() * 2 - 1, v = Math.sqrt(rand());
        let p = flowerTransform(petalPoint(layer, j, u, v, b.phase), b);
        let c = petalColour(layer, j, u, v, b);
        let edge = smooth(0.75, 1, v), isMist = rand() < 0.29;
        let fuzz = (isMist ? 0.038 : 0.010) * (1 + edge * 0.9);
        p = p.map(z => z + gaussian() * fuzz);
        let a = isMist ? 0.23 : 0.54;
        addParticle(p, c, a, 0.84 + rand() * 0.57, isMist ? 1.55 : 0.54, rand() * 100);
        if (k % 45 === 0) anchors.push({ p, c: lerpc(c, ivory, 0.38), v, seed: rand() * 100 });
      }
      for (let h = 0; h < 7; h++) {
        const v = 0.86 + rand() * 0.135, seed = rand() * 100; let prev = null;
        for (let step = 0; step < 24; step++) {
          const u = -1 + 2 * step / 23;
          let p = flowerTransform(petalPoint(layer, j, u, v + 0.008 * Math.sin(u * 12 + seed), b.phase), b);
          p = p.map((z, q) => z + 0.006 * Math.sin(u * 15 + seed + q * 2));
          if (prev) addThread(prev, p, [1, 0.84, 0.77], 0.115, 1.15, seed);
          prev = p;
        }
      }
      for (let h = 0; h < 13; h++) {
        let u = rand() * 2 - 1, start = 0.22 + rand() * 0.58, span = 0.10 + rand() * 0.26, prev = null;
        let col = petalColour(layer, j, u, 0.75, b), seed = rand() * 100;
        col = lerpc(col, ivory, 0.22);
        for (let s = 0; s < 14; s++) {
          let v = Math.min(0.999, start + span * s / 13);
          let p = flowerTransform(petalPoint(layer, j, u + 0.024 * Math.sin(s * 0.42 + seed), v, b.phase), b);
          if (prev) addThread(prev, p, col, 0.105, 0.85, seed);
          prev = p;
        }
      }
    }
  }
  for (let k = 0; k < 1000; k++) {
    let a = rand() * TAU, v = rand(), r = 0.025 + 0.07 * v;
    let p = flowerTransform([Math.sin(a) * r, 0.31 + 0.18 * (1 - v), Math.cos(a) * r], b);
    p = p.map(x => x + gaussian() * 0.015);
    addParticle(p, lerpc(coral, ivory, rand() * 0.45), 0.34, 1, 1.1);
  }
}

for (let j = 0; j < 15; j++) {
  let a = j * TAU / 15 + 0.28, seed = rand() * 100;
  for (let k = 0; k < 2400; k++) {
    let u = rand() * 2 - 1, v = Math.sqrt(rand());
    let r = 0.13 + 0.99 * Math.sin(v * 1.5), ang = a + u * 0.15 * Math.sin(Math.PI * v);
    let y = -0.78 + 0.69 * v + 0.09 * Math.sin(v * 4 + u * 3 + j);
    let p = [r * Math.sin(ang), y, r * Math.cos(ang)];
    p = p.map(x => x + gaussian() * 0.026);
    let c = lerpc([0.24, 0.27, 0.13], [0.79, 0.76, 0.55], smooth(0.25, 1, v));
    c = lerpc(c, [0.88, 0.79, 0.65], smooth(0.75, 1, Math.abs(u)) * 0.5);
    addParticle(p, c, 0.13, 0.95 + rand() * 0.6, 1.1, seed + rand());
  }
}

for (let k = 0; k < 42000; k++) {
  let a = rand() * TAU, v = rand(), y = -0.57 + 0.70 * v;
  let r = 1.07 * Math.sqrt(Math.max(0.01, 1 - Math.pow((y - 0.35) / 1.10, 2)));
  r += gaussian() * 0.047 + 0.055 * Math.sin(a * 7 + y * 12) + 0.035 * Math.sin(a * 13 - y * 8);
  let p = [r * Math.sin(a), y + gaussian() * 0.06, r * Math.cos(a)];
  let c = lerpc([0.23, 0.24, 0.115], [0.82, 0.77, 0.62], smooth(0.20, 0.95, v));
  c = lerpc(c, ivory, 0.24 * rand());
  addParticle(p, c, 0.24, 1.15 + rand() * 0.40, 1.5);
  if (k % 24 === 0) anchors.push({ p, c: lerpc(c, ivory, 0.28), v, seed: rand() * 100 });
}

for (let j = 0; j < 25; j++) {
  let a = j * TAU / 25, seed = rand() * 100;
  for (let k = 0; k < 520; k++) {
    let v = rand(), r = 0.035 + 0.16 * Math.pow(1 - v, 2) + 0.08 * smooth(0.70, 1, v) + 0.013 * Math.sin(v * 6 + seed), ang = a + 0.55 * v;
    let p = [r * Math.sin(ang) + gaussian() * 0.014, -1.56 + 0.94 * v, r * Math.cos(ang) + gaussian() * 0.014];
    let c = lerpc([0.57, 0.07, 0.12], [0.37, 0.28, 0.15], smooth(0.55, 1, v));
    addParticle(p, c, 0.32, 0.90 + rand() * 0.45, 1.4, seed + rand() * 3);
  }
}

function ribbonPoint(side, t, w) {
  const a = TAU * t;
  const x = side * (0.06 + 0.47 * Math.pow(Math.sin(a / 2), 1.15));
  const y = -1.005 + 0.105 * Math.sin(a) + w * 0.12 * (0.65 + 0.35 * Math.sin(a / 2));
  const z = 0.10 * Math.sin(a) + 0.18 * Math.sin(a / 2) + side * 0.025;
  return [x, y, z];
}

for (let side of [-1, 1]) {
  for (let k = 0; k < 7800; k++) {
    const t = rand(), w = rand() * 2 - 1;
    let p = ribbonPoint(side, t, w); p = p.map(x => x + gaussian() * 0.009);
    let c = lerpc([0.97, 0.88, 0.82], [1, 0.66, 0.72], 0.18 + 0.14 * Math.sin(t * TAU));
    addParticle(p, c, 0.41, 1.05, 1.4);
  }
  for (let j = 0; j < 45; j++) {
    let w = rand() * 2 - 1, prev = null, seed = rand() * 100;
    for (let s = 0; s < 60; s++) {
      let p = ribbonPoint(side, s / 59, w);
      if (prev) addThread(prev, p, [0.93, 0.80, 0.77], 0.065, 1.5, seed);
      prev = p;
    }
  }
  for (let k = 0; k < 1400; k++) {
    let t = rand(), w = (rand() - 0.5) * 0.065;
    let p = [side * (0.035 + 0.24 * t) + w, -1.035 - 0.35 * t + 0.06 * Math.sin(t * 6), 0.03 + 0.10 * Math.sin(t * 4)];
    addParticle(p, [0.79, 0.62, 0.62], 0.25, 1, 1.5);
  }
}

for (let j = 0; j < 4400; j++) {
  const a = anchors[Math.floor(rand() * anchors.length)];
  const phase = rand() * TAU, L = 0.065 + Math.pow(rand(), 2) * 0.34, radius = 0.008 + rand() * 0.027;
  const dir = normalize([gaussian(), 0.35 + gaussian() * 0.45, gaussian()]);
  const seed = rand() * 100; let prev = null;
  for (let k = 0; k < 18; k++) {
    let t = k / 17;
    let p = [
      a.p[0] + dir[0] * L * t + radius * Math.sin(t * 11 + phase) * t,
      a.p[1] + dir[1] * L * t + radius * Math.cos(t * 10 + phase) * t,
      a.p[2] + dir[2] * L * t + radius * Math.sin(t * 9 + phase + 1) * t
    ];
    let c = lerpc(a.c, ivory, 0.3);
    if (prev) addThread(prev, p, c, (0.048 + 0.026 * (1 - t)) * (1 - t * 0.6), 1.8, seed);
    if (k % 2 === 0) addParticle(p, c, 0.15 * (1 - t * 0.65), 1.05, 1.8, seed);
    prev = p;
  }
}

for (let k = 0; k < 7000; k++) {
  const a = anchors[Math.floor(rand() * anchors.length)];
  let spread = 0.05 + rand() * 0.08;
  const p = a.p.map(z => z + gaussian() * spread);
  addParticle(p, lerpc(a.c, ivory, 0.35), 0.11, 1.35 + rand() * 0.85, 2.6);
}

function shader(type, source) {
  const s = gl.createShader(type);
  gl.shaderSource(s, source);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw Error(gl.getShaderInfoLog(s));
  return s;
}
function program(v, f) {
  const p = gl.createProgram();
  gl.attachShader(p, shader(gl.VERTEX_SHADER, v));
  gl.attachShader(p, shader(gl.FRAGMENT_SHADER, f));
  gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw Error(gl.getProgramInfoLog(p));
  return p;
}

const vertexShader = `#version 300 es
precision highp float;
layout(location=0) in vec3 aPosition;
layout(location=1) in vec3 aColour;
layout(location=2) in vec4 aData;
uniform float uTime, uYaw, uPitch, uDistance, uAspect, uScale, uFlow, uPeriod, uXOffset;
uniform int uBox;
out vec3 vColour; out float vOpacity;

vec3 drift(vec3 p, float t) {
  vec3 q = p * 5.2;
  vec3 f = vec3(sin(q.y * 1.14 + q.z * 0.74 + t * 2.0), sin(q.z * 1.12 + q.x * 0.70 - t * 2.0), sin(q.x * 1.22 - q.y * 0.76 + t * 3.0));
  vec3 s = vec3(sin(q.y * 2.75 + f.z * 1.6 - t * 4.0), cos(q.z * 2.54 + f.x * 1.5 + t * 3.0), sin(q.x * 2.82 + f.y * 1.7 + t * 4.0));
  return f * 0.039 + s * 0.023;
}

void main() {
  vec3 p = aPosition;
  if (uBox == 0) {
    float t = uTime * 6.28318530718 / uPeriod;
    p += drift(p, t) * aData.z * uFlow;
    p += vec3(sin(t * 5.0 + aData.w), cos(t * 4.0 + aData.w * 1.3), sin(t * 6.0 + aData.w * 0.8)) * 0.004 * aData.z * uFlow;
    p.xz *= 1.0 + 0.006 * sin(t * 3.0 + p.y * 2.0);
  }
  float cy = cos(uYaw), sy = sin(uYaw);
  p = vec3(cy * p.x + sy * p.z, p.y, -sy * p.x + cy * p.z);
  float cp = cos(uPitch), sp = sin(uPitch);
  p = vec3(p.x, cp * p.y - sp * p.z, sp * p.y + cp * p.z);
  p.y += 0.035;
  p.x += uXOffset;

  float z = uDistance - p.z;
  float f = 3.35;
  gl_Position = vec4(p.x * f / uAspect, p.y * f, ((100.1 / 99.9) * z - (20.0 / 99.9)), z);
  gl_PointSize = clamp(aData.y * uScale * 11.4 / z, 0.7, 4.6 * uScale);
  float light = 0.82 + 0.18 * smoothstep(-1.2, 1.2, p.z);
  vColour = aColour * (uBox == 1 ? 1.0 : light);
  vOpacity = aData.x * (uBox == 1 ? 1.0 : (0.42 + 0.58 * smoothstep(-1.1, 1.1, p.z)));
}`;

const pointFragment = `#version 300 es
precision highp float;
in vec3 vColour; in float vOpacity;
out vec4 frag;
void main() {
  vec2 uv = (gl_PointCoord - 0.5) * 2.0;
  float r = dot(uv, uv);
  if (r > 1.0) discard;
  float a = exp(-r * 2.6) * (1.0 - smoothstep(0.72, 1.0, r));
  frag = vec4(vColour, a * vOpacity);
}`;

const lineFragment = `#version 300 es
precision highp float;
in vec3 vColour; in float vOpacity;
out vec4 frag;
void main() { frag = vec4(vColour, vOpacity); }`;

const pointsProgram = program(vertexShader, pointFragment);
const linesProgram = program(vertexShader, lineFragment);

function upload(vertices) {
  const vao = gl.createVertexArray();
  gl.bindVertexArray(vao);
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
  for (let [loc, num, offset] of [[0, 3, 0], [1, 3, 12], [2, 4, 24]]) {
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, num, gl.FLOAT, false, 40, offset);
  }
  return { vao, count: vertices.length / 10 };
}

const pointGeometry = upload(particles);
const threadGeometry = upload(threads);

const cage = [], cageDots = [];
const d = 1.52, low = -1.63, high = 1.75;
const corners = [
  [-d, low, -d], [d, low, -d], [d, low, d], [-d, low, d],
  [-d, high, -d], [d, high, -d], [d, high, d], [-d, high, d]
];
for (let [i, j] of [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]) {
  vertex(cage, corners[i], [0.65, 0.78, 0.92], 0.52, 1, 0, 0);
  vertex(cage, corners[j], [0.65, 0.78, 0.92], 0.52, 1, 0, 0);
}
for (let pt of corners) {
  vertex(cageDots, pt, [1, 1, 1], 0.95, 3.2, 0, 0);
}

const boxGeometry = upload(cage);
const boxDotsGeometry = upload(cageDots);
particles.length = 0; threads.length = 0;

const quadVertex = `#version 300 es
precision highp float;
out vec2 uv;
void main() {
  vec2 p = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));
  uv = p;
  gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0);
}`;

const blurFragment = `#version 300 es
precision highp float;
in vec2 uv;
uniform sampler2D image;
uniform vec2 stepUV;
uniform int firstPass;
out vec4 frag;
vec3 sampleAt(vec2 p) {
  vec3 c = texture(image, p).rgb;
  return firstPass == 1 ? max(c - 0.17, vec3(0.0)) : c;
}
void main() {
  vec3 c = sampleAt(uv) * 0.227027;
  c += sampleAt(uv + stepUV * 1.384615) * 0.316216;
  c += sampleAt(uv - stepUV * 1.384615) * 0.316216;
  c += sampleAt(uv + stepUV * 3.230769) * 0.070270;
  c += sampleAt(uv - stepUV * 3.230769) * 0.070270;
  frag = vec4(c, 1.0);
}`;

const finalFragment = `#version 300 es
precision highp float;
in vec2 uv;
uniform sampler2D scene, glow;
uniform float bloom, exposure;
out vec4 frag;
void main() {
  vec3 a = texture(scene, uv).rgb;
  vec3 b = texture(glow, uv).rgb;
  vec3 c = (a + b * bloom * 0.86) * exposure;
  vec2 v = (uv - 0.5) * vec2(1.33, 1.0);
  float vign = 1.0 - 0.15 * dot(v, v);
  c = vec3(1.0) - exp(-c * 1.18);
  c = pow(max(c, vec3(0.0)), vec3(0.83)) * vign;
  frag = vec4(clamp(c, 0.0, 1.0), 1.0);
}`;

const blurProgram = program(quadVertex, blurFragment);
const finalProgram = program(quadVertex, finalFragment);
const quadVAO = gl.createVertexArray();

const uniforms = new Map();
function loc(p, k) {
  let m = uniforms.get(p);
  if (!m) { m = {}; uniforms.set(p, m); }
  if (!(k in m)) m[k] = gl.getUniformLocation(p, k);
  return m[k];
}
function uniform(p, k, v) { gl.uniform1f(loc(p, k), v); }

function target(w, h) {
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texImage2D(gl.TEXTURE_2D, 0, HDR ? gl.RGBA16F : gl.RGBA8, w, h, 0, gl.RGBA, HDR ? gl.HALF_FLOAT : gl.UNSIGNED_BYTE, null);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  const fbo = gl.createFramebuffer();
  gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
  gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
  if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) !== gl.FRAMEBUFFER_COMPLETE) throw Error('Framebuffer unavailable');
  return { tex, fbo, w, h };
}

let sceneRT, blurA, blurB;
function resize(w, h) {
  const clientW = canvas.clientWidth || window.innerWidth || 1024;
  const clientH = canvas.clientHeight || window.innerHeight || 768;
  const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
  w = Math.round(w || Math.min(1920, Math.max(64, clientW * dpr)));
  h = Math.round(h || Math.max(48, clientH * dpr));
  if (canvas.width === w && canvas.height === h && sceneRT) return;
  canvas.width = w; canvas.height = h;
  for (const rt of [sceneRT, blurA, blurB]) {
    if (rt) { gl.deleteTexture(rt.tex); gl.deleteFramebuffer(rt.fbo); }
  }
  sceneRT = target(w, h);
  blurA = target(Math.ceil(w / 2), Math.ceil(h / 2));
  blurB = target(blurA.w, blurA.h);
}

function geometry(p, g, mode, t, isBox) {
  gl.useProgram(p);
  gl.bindVertexArray(g.vao);
  const angle = (PARAMS.spin ? t * TAU / PARAMS.duration : 0) + PARAMS.manualYaw + 0.25;
  const xOffset = PARAMS.codeVisible && window.innerWidth > 900 ? 0.70 : 0.0;
  uniform(p, 'uTime', t);
  uniform(p, 'uPeriod', PARAMS.duration);
  uniform(p, 'uYaw', angle);
  uniform(p, 'uPitch', PARAMS.cameraPitch + PARAMS.manualPitch);
  uniform(p, 'uDistance', PARAMS.cameraDistance);
  uniform(p, 'uAspect', canvas.width / canvas.height);
  uniform(p, 'uScale', canvas.height / 768);
  uniform(p, 'uFlow', PARAMS.flow);
  uniform(p, 'uXOffset', xOffset);
  gl.uniform1i(loc(p, 'uBox'), isBox ? 1 : 0);
  gl.drawArrays(mode, 0, g.count);
}

function blur(from, to, dx, dy, first) {
  gl.bindFramebuffer(gl.FRAMEBUFFER, to.fbo);
  gl.viewport(0, 0, to.w, to.h);
  gl.useProgram(blurProgram);
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, from.tex);
  gl.uniform1i(loc(blurProgram, 'image'), 0);
  gl.uniform2f(loc(blurProgram, 'stepUV'), dx, dy);
  gl.uniform1i(loc(blurProgram, 'firstPass'), first);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
}

function renderAt(t) {
  gl.bindFramebuffer(gl.FRAMEBUFFER, sceneRT.fbo);
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.disable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE);
  gl.clearColor(0.003, 0.005, 0.004, 1);
  gl.clear(gl.COLOR_BUFFER_BIT);

  if (PARAMS.box) {
    geometry(linesProgram, boxGeometry, gl.LINES, t, true);
    geometry(pointsProgram, boxDotsGeometry, gl.POINTS, t, true);
  }
  geometry(pointsProgram, pointGeometry, gl.POINTS, t, false);
  geometry(linesProgram, threadGeometry, gl.LINES, t, false);

  gl.disable(gl.BLEND);
  gl.bindVertexArray(quadVAO);
  blur(sceneRT, blurA, 1.5 / sceneRT.w, 0, 1);
  blur(blurA, blurB, 0, 1.7 / blurA.h, 0);
  blur(blurB, blurA, 2.1 / blurB.w, 0, 0);
  blur(blurA, blurB, 0, 2.1 / blurA.h, 0);

  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.useProgram(finalProgram);
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, sceneRT.tex);
  gl.uniform1i(loc(finalProgram, 'scene'), 0);
  gl.activeTexture(gl.TEXTURE1);
  gl.bindTexture(gl.TEXTURE_2D, blurB.tex);
  gl.uniform1i(loc(finalProgram, 'glow'), 1);
  uniform(finalProgram, 'bloom', PARAMS.bloom);
  uniform(finalProgram, 'exposure', PARAMS.exposure);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
}

let running = true, clock = 0, last = performance.now(), raf = 0;
function tick(now) {
  let dt = Math.min(0.1, (now - last) / 1000);
  last = now;
  if (!PARAMS.paused) clock += dt * PARAMS.speed;
  renderAt(clock);
  if (running) raf = requestAnimationFrame(tick);
}

resize();
renderAt(0);
if (running) raf = requestAnimationFrame(tick);

window.addEventListener('resize', () => resize());

// ==================== 3. 交互与控制按键 ====================
const $ = id => document.getElementById(id);

$('play').onclick = () => {
  PARAMS.paused = !PARAMS.paused;
  $('play').textContent = PARAMS.paused ? '播放' : '暂停';
};

$('spin').onclick = () => {
  PARAMS.manualYaw += (PARAMS.spin ? 1 : -1) * clock * TAU / PARAMS.duration;
  PARAMS.spin = !PARAMS.spin;
  $('spin').classList.toggle('active', PARAMS.spin);
};

$('box').onclick = () => {
  PARAMS.box = !PARAMS.box;
  $('box').classList.toggle('active', PARAMS.box);
};

$('code-btn').onclick = () => {
  PARAMS.codeVisible = !PARAMS.codeVisible;
  $('code-panel').classList.toggle('collapsed', !PARAMS.codeVisible);
  $('code-btn').classList.toggle('active', PARAMS.codeVisible);
};

function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {});
    $('fullscreen-btn').textContent = '⛶ 退出全屏';
  } else {
    if (document.exitFullscreen) document.exitFullscreen();
    $('fullscreen-btn').textContent = '⛶ 全屏模式';
  }
}
$('fullscreen-btn').onclick = toggleFullScreen;

$('options').onclick = () => {
  $('settings').style.display = $('settings').style.display === 'block' ? 'none' : 'block';
};

for (let id of ['speed', 'flow', 'bloom', 'exposure']) {
  $(id).oninput = e => {
    PARAMS[id] = +e.target.value;
    e.target.nextElementSibling.value = (+e.target.value).toFixed(2);
  };
}
$('scroll-speed').oninput = e => {
  scrollSpeed = (+e.target.value) * 0.6;
  $('scroll-speed').nextElementSibling.value = (+e.target.value).toFixed(2);
};

$('reset').onclick = () => {
  PARAMS.manualYaw = 0; PARAMS.manualPitch = 0; PARAMS.cameraDistance = 8.0; clock = 0;
};

$('snapshot').onclick = () => {
  renderAt(clock);
  canvas.toBlob(blob => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'particle-rose-fullscreen.png';
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }, 'image/png');
};

window.addEventListener('keydown', e => {
  if (e.code === 'Space' && e.target.tagName !== 'INPUT') {
    e.preventDefault(); $('play').click();
  }
  if (e.code === 'KeyS' && e.target.tagName !== 'INPUT') {
    toggleScrollState();
  }
  if (e.code === 'KeyB' && e.target.tagName !== 'INPUT') {
    $('box').click();
  }
  if (e.code === 'KeyC' && e.target.tagName !== 'INPUT') {
    $('code-btn').click();
  }
  if (e.code === 'KeyF' || e.code === 'F11') {
    e.preventDefault(); toggleFullScreen();
  }
  if (e.code === 'KeyH') document.body.classList.toggle('quiet');
});

// 鼠标 3D 旋转与视角推拉
let pointer = null;
canvas.addEventListener('pointerdown', e => {
  pointer = { x: e.clientX, y: e.clientY };
  canvas.setPointerCapture(e.pointerId);
});
canvas.addEventListener('pointermove', e => {
  if (pointer) {
    PARAMS.manualYaw += (e.clientX - pointer.x) * 0.006;
    PARAMS.manualPitch = clamp(PARAMS.manualPitch + (e.clientY - pointer.y) * 0.004, -0.6, 0.65);
    pointer = { x: e.clientX, y: e.clientY };
  }
});
canvas.addEventListener('pointerup', () => pointer = null);
canvas.addEventListener('pointercancel', () => pointer = null);
canvas.addEventListener('wheel', e => {
  e.preventDefault();
  PARAMS.cameraDistance = clamp(PARAMS.cameraDistance + e.deltaY * 0.003, 5.5, 11);
}, { passive: false });

let idle;
document.addEventListener('pointermove', () => {
  document.body.classList.remove('quiet');
  clearTimeout(idle);
  idle = setTimeout(() => {
    if ($('settings').style.display !== 'block') document.body.classList.add('quiet');
  }, 4500);
});
idle = setTimeout(() => document.body.classList.add('quiet'), 5000);
</script>
</body>
</html>"""

full_html = template.replace('__CODE_BODY__', code_html)
with open('particle_rose_fullscreen.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print('Created particle_rose_fullscreen.html, bytes:', len(full_html))

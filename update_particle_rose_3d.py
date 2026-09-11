import re

code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌹 3D 梦幻粒子玫瑰 · 极致浪漫视觉版 (多重唯美配色 + 花朵形态样式切换 + 原版源码自动滚动)
- 纯 Python + Tkinter 实现原生桌面全屏幕极客浪漫特效
- 左侧：自动无缝滚动播放原版 Python 核心源码与算法（带精美高亮与行号）
- 右侧：3D 全息线框立方体、超高密度粒子玫瑰花束、花瓣解离扩散与回流聚合
- 快捷键：
   [ESC] 退出/切换全屏 | [空格] 暂停旋转 | [D] 散开/聚合 | [S] 暂停滚动
   [C]   一键切换唯美配色 (红玫/粉钻/蓝妖/金珀/幽紫/冰晶/暗金)
   [V]   一键切换形态样式 (华美花束 / 唯美独秀 / 浪漫心形 / 星河旋涡)
   [B]   3D线框开关 | [T] 开关代码 | [H] 纯净模式 | [Q] 退出
"""

import tkinter as tk
from tkinter import font as tkfont
import math
import random
import time
import os
import re

# ==================== 1. 全局配置与 7 大唯美配色主题 ====================
FOV = 500                # 3D 投影视距
CUBE_SIZE = 160          # 3D 立方体线框半长

PALETTES = {
    "ruby_rose": {
        "name": "极品红玫 (热烈浪漫)",
        "edge": ["#ffffff", "#ffebee", "#ff80ab", "#ff4081", "#ffcdd2"],
        "petal_high": ["#ff1744", "#ff2a55", "#ff5252", "#f50057"],
        "petal_mid": ["#d50000", "#c51162", "#e91e63", "#ad1457"],
        "petal_dark": ["#880e4f", "#4a001f", "#5c001e", "#3a0010"],
        "core": ["#fff9c4", "#fff59d", "#ffffff", "#ffe082"],
        "sepal": ["#2e7d32", "#4caf50", "#388e3c", "#1b5e20"],
        "stem": ["#b71c1c", "#880e4f", "#5c001e", "#3a0010"],
        "ribbon": ["#ffffff", "#fff0f3", "#ffd6e0", "#ffccd5"],
        "cube": "#6888b0",
        "cube_dot": "#e2edff",
        "bg": "#04060a"
    },
    "blue_enchantress": {
        "name": "蓝色妖姬 (冷艳极光)",
        "edge": ["#ffffff", "#e0fbfc", "#caf0f8", "#90e0ef"],
        "petal_high": ["#00b4d8", "#0077b6", "#48cae4", "#0096c7"],
        "petal_mid": ["#023e8a", "#03045e", "#0077b6", "#1d3557"],
        "petal_dark": ["#050c1e", "#0b132b", "#1c2541"],
        "core": ["#ffffff", "#e0fbfc", "#caf0f8"],
        "sepal": ["#1b4332", "#2d6a4f", "#40916c"],
        "stem": ["#03045e", "#0a192f", "#021226"],
        "ribbon": ["#e0fbfc", "#ffffff", "#90e0ef"],
        "cube": "#4088b0",
        "cube_dot": "#ccf0ff",
        "bg": "#03070d"
    },
    "pink_diamond": {
        "name": "粉钻甜心 (娇艳柔美)",
        "edge": ["#ffffff", "#fff0f3", "#ffd6e0", "#ffccd5"],
        "petal_high": ["#ff758f", "#ff8fa3", "#ffb3c1", "#ff4d6d"],
        "petal_mid": ["#c9184a", "#a4133c", "#ff4d6d", "#d90429"],
        "petal_dark": ["#590d22", "#800f2f", "#400817"],
        "core": ["#ffffff", "#fff0f3", "#ffccd5"],
        "sepal": ["#388e3c", "#4caf50", "#2e7d32"],
        "stem": ["#800f2f", "#590d22", "#38000f"],
        "ribbon": ["#ffffff", "#ffe5ec", "#ffb3c1"],
        "cube": "#8a6d9e",
        "cube_dot": "#f0e6ff",
        "bg": "#08050d"
    },
    "golden_amber": {
        "name": "流光香槟 (轻奢香槟金)",
        "edge": ["#ffffff", "#fef9e7", "#fcf3cf", "#f9e79f"],
        "petal_high": ["#f1c40f", "#f39c12", "#f5b041", "#f8c471"],
        "petal_mid": ["#d4ac0d", "#b7950b", "#d68910", "#ba4a00"],
        "petal_dark": ["#784212", "#6e2c00", "#4d2800"],
        "core": ["#ffffff", "#fef9e7"],
        "sepal": ["#33691e", "#558b2f", "#2e7d32"],
        "stem": ["#6e2c00", "#4d2800", "#301800"],
        "ribbon": ["#ffffff", "#fcf3cf", "#f9e79f"],
        "cube": "#8a7548",
        "cube_dot": "#fff6dc",
        "bg": "#0a0805"
    },
    "aurora_purple": {
        "name": "极光幽紫 (梦幻星云)",
        "edge": ["#ffffff", "#f3e8ff", "#e9d5ff", "#d8b4fe"],
        "petal_high": ["#c084fc", "#a855f7", "#9333ea", "#7e22ce"],
        "petal_mid": ["#7e22ce", "#6b21a8", "#581c87", "#4c1d95"],
        "petal_dark": ["#2e1065", "#1e0842", "#13042b"],
        "core": ["#ffffff", "#f3e8ff", "#d8b4fe"],
        "sepal": ["#164e63", "#0891b2", "#0e7490"],
        "stem": ["#3b0764", "#2e1065", "#170329"],
        "ribbon": ["#f3e8ff", "#ffffff", "#c084fc"],
        "cube": "#8b5cf6",
        "cube_dot": "#ede9fe",
        "bg": "#07040d"
    },
    "crystal_white": {
        "name": "初雪冰晶 (晶莹钻石白)",
        "edge": ["#ffffff", "#f8fafc", "#f1f5f9", "#e2e8f0"],
        "petal_high": ["#e2e8f0", "#cbd5e1", "#94a3b8", "#e0f2fe"],
        "petal_mid": ["#64748b", "#475569", "#334155", "#0284c7"],
        "petal_dark": ["#1e293b", "#0f172a", "#020617"],
        "core": ["#ffffff", "#f0f9ff", "#e0f2fe"],
        "sepal": ["#334155", "#475569", "#1e293b"],
        "stem": ["#1e293b", "#0f172a", "#020617"],
        "ribbon": ["#ffffff", "#f1f5f9", "#cbd5e1"],
        "cube": "#7dd3fc",
        "cube_dot": "#f0f9ff",
        "bg": "#04070a"
    },
    "black_gold": {
        "name": "暗夜流火 (熔岩赛博金)",
        "edge": ["#ffffff", "#ffedd5", "#fed7aa", "#f97316"],
        "petal_high": ["#ea580c", "#c2410c", "#9a3412", "#fbbf24"],
        "petal_mid": ["#7c2d12", "#431407", "#290c04", "#d97706"],
        "petal_dark": ["#1c0802", "#110401", "#050100"],
        "core": ["#fef08a", "#facc15", "#ffffff"],
        "sepal": ["#27272a", "#3f3f46", "#18181b"],
        "stem": ["#290c04", "#110401", "#050100"],
        "ribbon": ["#fed7aa", "#f97316", "#ffffff"],
        "cube": "#f97316",
        "cube_dot": "#ffedd5",
        "bg": "#080503"
    }
}

STYLES = {
    "bouquet": "💐 华美花束 (11朵层叠花簇)",
    "single":  "🌹 唯美独秀 (巨型深杯单朵特写)",
    "heart":   "💖 浪漫心形 (爱心轮廓花束)",
    "cosmic":  "🌌 星河旋涡 (大螺旋旋流花阵)"
}

current_theme = "ruby_rose"
current_style = "bouquet"

# ==================== 2. 代码高亮词法解析器 ====================
KEYWORDS = {
    'def', 'class', 'import', 'from', 'return', 'for', 'in', 'if', 'elif', 'else',
    'while', 'try', 'except', 'global', 'lambda', 'as', 'with', 'pass', 'True', 'False',
    'None', 'not', 'and', 'or', 'is'
}
BUILTINS = {'range', 'len', 'int', 'float', 'str', 'set', 'list', 'dict', 'print', 'max', 'min', 'abs', 'round', 'time', 'math', 'random'}
SPECIAL_ATTRS = {'self'}

TOKEN_REGEX = re.compile(
    r'(?P<COMMENT>#.*$)'
    r'|(?P<STRING>f?"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\')'
    r'|(?P<NUMBER>\\b\\d+\\.?\\d*(?:e[+-]?\\d+)?\\b)'
    r'|(?P<WORD>[a-zA-Z_]\\w*)'
    r'|(?P<OP>[+\\-*/%&|^~<>=!:]+)'
    r'|(?P<PUNC>[()[\\]{},;.])'
    r'|(?P<SPACE>\\s+)'
    r'|(?P<OTHER>.)'
)

def tokenize_code_line(line):
    tokens = []
    prev_word = None
    for match in TOKEN_REGEX.finditer(line):
        kind = match.lastgroup
        val = match.group()
        if kind == 'COMMENT':
            col = '#6272a4'
        elif kind == 'STRING':
            col = '#50fa7b'
        elif kind == 'NUMBER':
            col = '#ffb86c'
        elif kind == 'WORD':
            if val in KEYWORDS:
                col = '#ff5370'
            elif val in BUILTINS:
                col = '#f1fa8c'
            elif val in SPECIAL_ATTRS:
                col = '#ff79c6'
            elif prev_word == 'def':
                col = '#8be9fd'
            elif prev_word == 'class':
                col = '#f1fa8c'
            else:
                col = '#abb2bf'
            prev_word = val
            tokens.append((val, col))
            continue
        elif kind == 'OP':
            col = '#80cbc4'
        elif kind == 'PUNC':
            col = '#6c7891'
        elif kind == 'SPACE':
            col = '#abb2bf'
        else:
            col = '#abb2bf'
        tokens.append((val, col))
        if kind != 'SPACE':
            prev_word = None
            
    merged = []
    for txt, col in tokens:
        if merged and merged[-1][1] == col:
            merged[-1] = (merged[-1][0] + txt, col)
        else:
            merged.append((txt, col))
    return merged

def load_original_code():
    source_file = "particle_rose_3d.py.bak"
    if not os.path.exists(source_file):
        source_file = os.path.abspath(__file__)
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            raw_lines = [l.replace('\\t', '    ').rstrip('\\r\\n') for l in f]
    except Exception:
        raw_lines = [
            "# 3D Mathematical Parametric Rose",
            "p = (math.pi / 2.0) * math.exp(-t / (8.0 * math.pi))",
            "u_factor = 1.0 - ((1.0 - mod_t / math.pi) ** 4) / 2.0"
        ]
    tokenized = [tokenize_code_line(l) for l in raw_lines]
    return raw_lines, tokenized

# ==================== 3. 3D 多形态粒子玫瑰花束建模 ====================
def generate_perfect_rose_bouquet(total_points=6200, style="bouquet"):
    pal = PALETTES[current_theme]
    particles = []

    if style == "single":
        flowers = [{"x": 0.0, "y": -15.0, "z": 0.0, "scale": 1.75, "tilt": 0.15, "az": 0.0, "phase": 0.2}]
    elif style == "heart":
        flowers = [{"x": 0.0, "y": 18.0, "z": 0.0, "scale": 0.92, "tilt": 0.0, "az": 0.0, "phase": 0.2}]
        for j in range(6):
            t_h = j * (math.pi * 2 / 6.0)
            hx = 54.0 * (math.sin(t_h) ** 3)
            hz = -46.0 * (13 * math.cos(t_h) - 5 * math.cos(2*t_h) - 2 * math.cos(3*t_h) - math.cos(4*t_h)) / 16.0
            flowers.append({
                "x": hx, "y": 8.0 + 3.0 * math.sin(t_h*2), "z": hz,
                "scale": 0.78, "tilt": 0.62, "az": math.atan2(hx, hz),
                "phase": random.uniform(0, math.pi * 2)
            })
    elif style == "cosmic":
        flowers = [{"x": 0.0, "y": 20.0, "z": 0.0, "scale": 0.95, "tilt": 0.0, "az": 0.0, "phase": 0.2}]
        for j in range(6):
            r_sp = 25.0 + j * 11.0
            ang = j * 0.95
            flowers.append({
                "x": r_sp * math.sin(ang), "y": 12.0 - j * 6.0, "z": r_sp * math.cos(ang),
                "scale": 0.78, "tilt": 0.75, "az": ang,
                "phase": random.uniform(0, math.pi * 2)
            })
    else:  # bouquet
        flowers = [{"x": 0.0, "y": 28.0, "z": 0.0, "scale": 1.05, "tilt": 0.0, "az": 0.0, "phase": 0.2}]
        for j in range(5):
            ang = j * (math.pi * 2 / 5.0) + 0.35
            dist = 52.0
            flowers.append({
                "x": dist * math.sin(ang),
                "y": 6.0 + 4.0 * math.sin(ang * 2),
                "z": dist * math.cos(ang),
                "scale": 0.88,
                "tilt": 0.52,
                "az": ang,
                "phase": random.uniform(0, math.pi * 2)
            })

    points_per_flower = int((total_points * 0.65) / len(flowers))

    for fl in flowers:
        cos_az, sin_az = math.cos(fl["az"]), math.sin(fl["az"])
        cos_ti, sin_ti = math.cos(fl["tilt"]), math.sin(fl["tilt"])

        for _ in range(points_per_flower):
            t_norm = random.uniform(0, 1) ** 0.82
            t = t_norm * (20.0 * math.pi) + 3.8 * math.pi
            p = (math.pi / 2.0) * math.exp(-t / (8.0 * math.pi))
            ripple = math.sin(15.0 * t) / 140.0

            mod_t = (3.4 * t) % (2.0 * math.pi)
            u_factor = 1.0 - ((1.0 - mod_t / math.pi) ** 4) / 2.0 + ripple

            is_edge = random.random() < 0.34
            if is_edge:
                x = random.uniform(0.85, 1.0)
            else:
                x = random.uniform(0.08, 0.95)

            y_prof = 2.0 * (x**2 - x) ** 2 * math.sin(p)
            r = u_factor * (x * math.sin(p) + y_prof * math.cos(p))
            h = u_factor * (x * math.cos(p) - y_prof * math.sin(p))

            sc = 95.0 * fl["scale"]
            bx = r * math.cos(t) * sc
            bz = r * math.sin(t) * sc
            by = (h * sc) - 15.0

            rx1 = bx * cos_az + by * sin_az * sin_ti + bz * sin_az * cos_ti
            ry1 = by * cos_ti - bz * sin_ti
            rz1 = -bx * sin_az + by * cos_az * sin_ti + bz * cos_az * cos_ti

            world_x = fl["x"] + rx1
            world_y = fl["y"] + ry1
            world_z = fl["z"] + rz1

            dist_c = math.sqrt(bx**2 + bz**2)
            if is_edge:
                col = random.choice(pal["edge"])
                size = 2 if random.random() < 0.35 else 1
            elif dist_c < 20 and by > -10:
                col = random.choice(pal["core"])
                size = 2 if random.random() < 0.25 else 1
            elif dist_c < 55:
                col = random.choice(pal["petal_high"])
                size = 1
            elif x < 0.35 or by < -15:
                col = random.choice(pal["petal_dark"])
                size = 1
            else:
                col = random.choice(pal["petal_mid"])
                size = 1

            rad_norm = math.sqrt(world_x**2 + world_z**2 + 1e-6)
            dir_x = (world_x / rad_norm) * 0.75 - (world_z / rad_norm) * 0.45
            dir_z = (world_z / rad_norm) * 0.75 + (world_x / rad_norm) * 0.45
            dir_y = (world_y / 120.0) * 0.4 + random.uniform(-0.3, 0.5)

            particles.append({
                "hx": world_x, "hy": world_y, "hz": world_z,
                "col": col, "size": size, "part": "petal",
                "phase": random.uniform(0, math.pi * 2),
                "dir_x": dir_x, "dir_y": dir_y, "dir_z": dir_z,
                "diff_speed": random.uniform(0.6, 1.4)
            })

    # 萼片
    sepal_points = int(total_points * 0.12)
    for _ in range(sepal_points):
        theta = random.uniform(0, 2 * math.pi)
        v = math.sqrt(random.uniform(0, 1))
        r_sepal = 18.0 + 65.0 * math.sin(v * 1.5)
        leaf_mod = abs(math.sin(theta * 5.0)) ** 0.65
        r_sepal *= (0.6 + 0.4 * leaf_mod)
        bx = r_sepal * math.cos(theta) + random.gauss(0, 2)
        bz = r_sepal * math.sin(theta) + random.gauss(0, 2)
        by = -48.0 + 38.0 * v + random.gauss(0, 2)
        col = random.choice(pal["sepal"])
        particles.append({
            "hx": bx, "hy": by, "hz": bz, "col": col, "size": 1, "part": "sepal",
            "phase": random.uniform(0, math.pi * 2),
            "dir_x": (bx / (abs(bx) + abs(bz) + 1e-4)), "dir_y": -0.2, "dir_z": (bz / (abs(bx) + abs(bz) + 1e-4)),
            "diff_speed": random.uniform(0.4, 0.9)
        })

    # 丝带
    ribbon_points = int(total_points * 0.06)
    for _ in range(ribbon_points):
        side = random.choice([-1, 1])
        t_rib = random.uniform(0, math.pi * 2)
        w = random.uniform(-1, 1)
        bx = side * (8.0 + 45.0 * (abs(math.sin(t_rib / 2.0)) ** 1.15))
        by = -68.0 + 10.0 * math.sin(t_rib) + w * 12.0
        bz = 14.0 * math.sin(t_rib) + 18.0 * math.sin(t_rib / 2.0) + side * 4.0
        col = random.choice(pal["ribbon"])
        particles.append({
            "hx": bx, "hy": by, "hz": bz, "col": col, "size": 1, "part": "ribbon",
            "phase": random.uniform(0, math.pi * 2),
            "dir_x": bx * 0.02, "dir_y": 0.1, "dir_z": bz * 0.02, "diff_speed": random.uniform(0.5, 1.1)
        })

    # 花茎
    stem_points = int(total_points * 0.11)
    for _ in range(stem_points):
        v = random.uniform(0, 1)
        ang = random.uniform(0, 2 * math.pi)
        r_stem = 5.0 + 26.0 * ((1.0 - v) ** 1.8) + random.gauss(0, 1.5)
        bx = r_stem * math.cos(ang) + random.gauss(0, 1.5)
        bz = r_stem * math.sin(ang) + random.gauss(0, 1.5)
        by = -148.0 + 82.0 * v
        col = random.choice(pal["stem"])
        particles.append({
            "hx": bx, "hy": by, "hz": bz, "col": col, "size": 1, "part": "stem",
            "phase": random.uniform(0, math.pi * 2),
            "dir_x": bx * 0.02, "dir_y": -0.4, "dir_z": bz * 0.02, "diff_speed": random.uniform(0.3, 0.7)
        })

    # 星尘
    ember_points = int(total_points * 0.06)
    for _ in range(ember_points):
        rx = random.uniform(-CUBE_SIZE * 0.95, CUBE_SIZE * 0.95)
        ry = random.uniform(-CUBE_SIZE * 0.95, CUBE_SIZE * 0.95)
        rz = random.uniform(-CUBE_SIZE * 0.95, CUBE_SIZE * 0.95)
        col = random.choice(pal["edge"])
        particles.append({
            "hx": rx, "hy": ry, "hz": rz, "col": col, "size": 1, "part": "ember",
            "phase": random.uniform(0, math.pi * 2),
            "dir_x": random.uniform(-1, 1), "dir_y": random.uniform(-0.5, 1), "dir_z": random.uniform(-1, 1),
            "diff_speed": random.uniform(0.8, 1.6)
        })

    return particles

CUBE_VERTICES = [
    [-CUBE_SIZE, -CUBE_SIZE * 1.05, -CUBE_SIZE],
    [ CUBE_SIZE, -CUBE_SIZE * 1.05, -CUBE_SIZE],
    [ CUBE_SIZE,  CUBE_SIZE * 1.15, -CUBE_SIZE],
    [-CUBE_SIZE,  CUBE_SIZE * 1.15, -CUBE_SIZE],
    [-CUBE_SIZE, -CUBE_SIZE * 1.05,  CUBE_SIZE],
    [ CUBE_SIZE, -CUBE_SIZE * 1.05,  CUBE_SIZE],
    [ CUBE_SIZE,  CUBE_SIZE * 1.15,  CUBE_SIZE],
    [-CUBE_SIZE,  CUBE_SIZE * 1.15,  CUBE_SIZE],
]

CUBE_EDGES = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

# ==================== 4. 原生桌面全屏应用主程序 ====================
class FullscreenRoseApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3D 粒子玫瑰 · 多重唯美配色与形态全屏盛宴")

        self.is_fullscreen = True
        self.root.attributes("-fullscreen", True)
        
        try:
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.after(800, lambda: self.root.attributes("-topmost", False))
            self.root.focus_force()
        except Exception:
            pass

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        pal = PALETTES[current_theme]
        self.root.configure(bg=pal["bg"])

        self.canvas = tk.Canvas(
            self.root, width=self.screen_w, height=self.screen_h,
            bg=pal["bg"], highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.code_font = tkfont.Font(family="Menlo", size=11)
        self.code_char_w = self.code_font.measure("m")
        self.code_line_h = 22

        self.code_raw, self.code_tokens = load_original_code()
        self.total_code_lines = len(self.code_tokens)
        self.scroll_y = 0.0
        self.scroll_speed = 0.55
        self.auto_scroll = True

        self.rot_x = 0.42
        self.rot_y = 0.48
        self.zoom = 1.08
        self.auto_rotate = True
        self.show_box = True
        self.show_code = True
        self.show_hud = True
        self.is_running = True

        self.diffuse_burst = 0.0
        self.manual_burst_time = -999.0
        self.diffusion_duration = 16.0

        self.last_mx = 0
        self.last_my = 0
        self.is_dragging = False

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.root.bind("<Escape>", lambda e: self.toggle_fullscreen())
        self.root.bind("<f>", lambda e: self.toggle_fullscreen())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<space>", lambda e: self.toggle_rotate())
        self.root.bind("<d>", lambda e: self.trigger_burst())
        self.root.bind("<D>", lambda e: self.trigger_burst())
        self.root.bind("<s>", lambda e: self.toggle_scroll())
        self.root.bind("<S>", lambda e: self.toggle_scroll())
        self.root.bind("<c>", lambda e: self.switch_theme())
        self.root.bind("<C>", lambda e: self.switch_theme())
        self.root.bind("<v>", lambda e: self.switch_style())
        self.root.bind("<V>", lambda e: self.switch_style())
        self.root.bind("<b>", lambda e: self.toggle_box())
        self.root.bind("<B>", lambda e: self.toggle_box())
        self.root.bind("<t>", lambda e: self.toggle_code())
        self.root.bind("<T>", lambda e: self.toggle_code())
        self.root.bind("<h>", lambda e: self.toggle_hud())
        self.root.bind("<H>", lambda e: self.toggle_hud())
        self.root.bind("<plus>", lambda e: self.adjust_zoom(0.08))
        self.root.bind("<equal>", lambda e: self.adjust_zoom(0.08))
        self.root.bind("<minus>", lambda e: self.adjust_zoom(-0.08))
        self.root.bind("<q>", lambda e: self.on_close())
        self.root.bind("<Q>", lambda e: self.on_close())
        self.root.bind("<Configure>", self.on_resize)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.particles = generate_perfect_rose_bouquet(style=current_style)
        self.start_time = time.time()
        self.render_loop()

    def on_resize(self, event):
        if event.widget == self.root:
            self.screen_w = max(400, event.width)
            self.screen_h = max(300, event.height)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def toggle_rotate(self):
        self.auto_rotate = not self.auto_rotate

    def toggle_scroll(self):
        self.auto_scroll = not self.auto_scroll

    def toggle_box(self):
        self.show_box = not self.show_box

    def toggle_code(self):
        self.show_code = not self.show_code

    def toggle_hud(self):
        self.show_hud = not self.show_hud

    def trigger_burst(self):
        self.manual_burst_time = time.time() - self.start_time

    def adjust_zoom(self, delta):
        self.zoom = max(0.5, min(2.5, self.zoom + delta))

    def switch_theme(self):
        global current_theme
        keys = list(PALETTES.keys())
        idx = (keys.index(current_theme) + 1) % len(keys)
        current_theme = keys[idx]
        pal = PALETTES[current_theme]
        self.root.configure(bg=pal["bg"])
        self.canvas.configure(bg=pal["bg"])
        self.particles = generate_perfect_rose_bouquet(style=current_style)

    def switch_style(self):
        global current_style
        styles = list(STYLES.keys())
        idx = (styles.index(current_style) + 1) % len(styles)
        current_style = styles[idx]
        self.particles = generate_perfect_rose_bouquet(style=current_style)

    def on_mouse_down(self, event):
        self.is_dragging = True
        self.last_mx = event.x
        self.last_my = event.y

    def on_mouse_drag(self, event):
        if self.is_dragging:
            dx = event.x - self.last_mx
            dy = event.y - self.last_my
            self.rot_y += dx * 0.007
            self.rot_x -= dy * 0.007
            self.last_mx = event.x
            self.last_my = event.y

    def on_mouse_up(self, event):
        self.is_dragging = False

    def on_mouse_wheel(self, event):
        if event.x < self.screen_w * 0.38:
            self.scroll_y -= event.delta * 2.0
            if self.scroll_y < 0:
                self.scroll_y = 0
        else:
            delta = 0.06 if event.delta > 0 else -0.06
            self.adjust_zoom(delta)

    def on_close(self):
        self.is_running = False
        try:
            self.root.destroy()
        except Exception:
            pass

    def project_3d(self, x, y, z, cx, cy):
        cos_x, sin_x = math.cos(self.rot_x), math.sin(self.rot_x)
        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x

        cos_y, sin_y = math.cos(self.rot_y), math.sin(self.rot_y)
        x2 = x * cos_y + z1 * sin_y
        z2 = -x * sin_y + z1 * cos_y

        cam_dist = 480
        depth = z2 + cam_dist
        if depth <= 15:
            depth = 15
        factor = (FOV * self.zoom) / depth
        screen_x = cx + x2 * factor
        screen_y = cy - y1 * factor
        return screen_x, screen_y, z2

    def calculate_diffusion(self, t):
        cycle = (t % self.diffusion_duration) / self.diffusion_duration
        if cycle < 0.22:
            auto = 0.0
        elif cycle < 0.52:
            k = (cycle - 0.22) / 0.30
            auto = k * k * (3 - 2 * k)
        elif cycle < 0.88:
            k = 1.0 - (cycle - 0.52) / 0.36
            auto = k * k * (3 - 2 * k)
        else:
            auto = 0.0

        since = t - self.manual_burst_time
        if 0 <= since < 6.0:
            if since < 1.2:
                k = since / 1.2
                manual = k * k * (3 - 2 * k)
            else:
                k = 1.0 - (since - 1.2) / 4.8
                manual = k * k * (3 - 2 * k)
        else:
            manual = 0.0

        return max(auto, manual)

    def draw_scrolling_code(self, panel_w, panel_h):
        self.canvas.create_rectangle(0, 0, panel_w, panel_h, fill="#060911", outline="")
        self.canvas.create_line(panel_w, 0, panel_w, panel_h, fill="#162032", width=1)

        tab_h = 38
        self.canvas.create_rectangle(0, 0, panel_w, tab_h, fill="#090d18", outline="")
        self.canvas.create_line(0, tab_h, panel_w, tab_h, fill="#162032", width=1)

        self.canvas.create_oval(14, 13, 24, 23, fill="#ff5f56", outline="")
        self.canvas.create_oval(30, 13, 40, 23, fill="#ffbd2e", outline="")
        self.canvas.create_oval(46, 13, 56, 23, fill="#27c93f", outline="")

        self.canvas.create_text(
            72, 18,
            text="●  particle_rose_3d.py (Python 原版源码 · 自动滚动)",
            fill="#8b9eb7", font=("Menlo", 10), anchor="w"
        )

        content_top = tab_h + 12
        content_bottom = panel_h - 10
        total_px = self.total_code_lines * self.code_line_h

        cur_y_offset = self.scroll_y % total_px
        start_idx = int(cur_y_offset // self.code_line_h)
        pixel_drift = cur_y_offset % self.code_line_h

        visible_count = int((content_bottom - content_top) // self.code_line_h) + 3

        line_num_x = 42
        self.canvas.create_line(line_num_x + 8, content_top - 12, line_num_x + 8, panel_h, fill="#121a28", width=1)

        for i in range(visible_count):
            line_idx = (start_idx + i) % self.total_code_lines
            line_num = line_idx + 1
            y = content_top + i * self.code_line_h - pixel_drift

            if y < content_top - self.code_line_h or y > content_bottom:
                continue

            self.canvas.create_text(line_num_x, y, text=str(line_num), fill="#314156", font=self.code_font, anchor="ne")

            tokens = self.code_tokens[line_idx]
            token_x = line_num_x + 18
            for text, col in tokens:
                if token_x > panel_w - 20:
                    break
                self.canvas.create_text(token_x, y, text=text, fill=col, font=self.code_font, anchor="nw")
                token_x += len(text) * self.code_char_w

    def render_loop(self):
        if not self.is_running:
            return

        t = time.time() - self.start_time
        pal = PALETTES[current_theme]

        if self.auto_rotate and not self.is_dragging:
            self.rot_y += 0.009
            self.rot_x = 0.42 + 0.06 * math.sin(t * 0.45)

        if self.auto_scroll and self.show_code:
            self.scroll_y += self.scroll_speed

        burst = self.calculate_diffusion(t)
        pulse = 1.0 + 0.045 * math.sin(t * 2.4) * (abs(math.cos(t * 2.4)) ** 0.5)

        self.canvas.delete("all")

        code_panel_w = int(self.screen_w * 0.38) if self.show_code else 0
        if self.show_code:
            self.draw_scrolling_code(code_panel_w, self.screen_h)

        center_x = (code_panel_w + self.screen_w) * 0.50 if self.show_code else self.screen_w * 0.50
        center_y = self.screen_h * 0.50

        if self.show_box:
            proj_cube = []
            for vx, vy, vz in CUBE_VERTICES:
                sx, sy, sz = self.project_3d(vx, vy, vz, center_x, center_y)
                proj_cube.append((sx, sy, sz))

            for i, j in CUBE_EDGES:
                x1, y1, z1 = proj_cube[i]
                x2, y2, z2 = proj_cube[j]
                avg_z = (z1 + z2) / 2
                edge_col = pal["cube"] if avg_z < 0 else "#253a52"
                self.canvas.create_line(x1, y1, x2, y2, fill=edge_col, width=1.4)

            dot_col = pal["cube_dot"]
            for sx, sy, sz in proj_cube:
                r_dot = 3 if sz > 0 else 2
                self.canvas.create_oval(
                    sx - r_dot, sy - r_dot, sx + r_dot, sy + r_dot,
                    fill=dot_col, outline=pal["cube"]
                )

        render_queue = []
        for p in self.particles:
            hx, hy, hz = p["hx"], p["hy"], p["hz"]

            if p["part"] == "petal":
                wobble = 1.0 + 0.02 * math.sin(t * 3.2 + p["phase"])
                base_x = hx * pulse * wobble
                base_y = hy * pulse * wobble
                base_z = hz * pulse * wobble

                if burst > 0.001:
                    travel = (burst ** 1.08) * p["diff_speed"] * 145.0
                    fine_w = math.sin(t * 3.5 + p["phase"])
                    px = base_x + p["dir_x"] * travel + fine_w * travel * 0.25
                    py = base_y + p["dir_y"] * travel + math.cos(t * 3.0 + p["phase"]) * travel * 0.25
                    pz = base_z + p["dir_z"] * travel + math.sin(t * 2.8 + p["phase"] * 2) * travel * 0.25
                else:
                    px, py, pz = base_x, base_y, base_z

            elif p["part"] == "stem" or p["part"] == "sepal":
                px = hx * (1.0 + 0.012 * pulse)
                py = hy
                pz = hz * (1.0 + 0.012 * pulse)
                if burst > 0.001:
                    travel = (burst ** 1.1) * p["diff_speed"] * 35.0
                    px += p["dir_x"] * travel
                    py += p["dir_y"] * travel
                    pz += p["dir_z"] * travel

            elif p["part"] == "ribbon":
                wobble = math.sin(t * 2.0 + p["phase"]) * 1.5
                px = hx + wobble
                py = hy
                pz = hz + wobble
                if burst > 0.001:
                    travel = (burst ** 1.08) * p["diff_speed"] * 75.0
                    px += p["dir_x"] * travel
                    py += p["dir_y"] * travel
                    pz += p["dir_z"] * travel

            else:
                drift = math.sin(t * 1.2 + p["phase"]) * 8.0
                px = hx + drift + (p["dir_x"] * burst * 90.0)
                py = hy + math.cos(t * 1.4 + p["phase"]) * 8.0 + (p["dir_y"] * burst * 90.0)
                pz = hz + drift + (p["dir_z"] * burst * 90.0)

            sx, sy, sz = self.project_3d(px, py, pz, center_x, center_y)
            render_queue.append((sz, sx, sy, p["col"], p["size"], p["part"]))

        render_queue.sort(key=lambda item: item[0], reverse=True)

        for sz, sx, sy, col, size, part in render_queue:
            if sz < -90 and size > 1:
                size = 1
            elif sz > 80 and size == 1 and random.random() < 0.15:
                size = 2

            if size == 1:
                self.canvas.create_rectangle(sx, sy, sx + 1.2, sy + 1.2, outline=col, fill=col)
            elif size == 2:
                self.canvas.create_oval(sx - 1.2, sy - 1.2, sx + 1.2, sy + 1.2, outline=col, fill=col)
            else:
                self.canvas.create_oval(sx - 1.8, sy - 1.8, sx + 1.8, sy + 1.8, outline=col, fill=col)

        if self.show_hud:
            info = f"🎨 [C] 换颜色: {pal['name']} | ✨ [V] 换样式: {STYLES[current_style]} | [ESC] 全屏 | [D] 扩散 | [S] 代码滚动 | [B] 线框 | [H] 纯净"
            self.canvas.create_text(
                self.screen_w // 2, self.screen_h - 24,
                text=info, fill="#4e627d", font=("Helvetica", 11)
            )

        try:
            self.root.after(16, self.render_loop)
        except Exception:
            pass

if __name__ == "__main__":
    print("=" * 65)
    print("🌹 正在本地启动全屏 3D 粒子玫瑰 (支持多重唯美配色 + 形态切换)...")
    print("💡 快捷键提示:")
    print("   [C]     一键切换唯美配色 (红玫/蓝妖/粉钻/香槟/幽紫/冰晶/暗金)")
    print("   [V]     一键切换花朵形态 (华美花束 / 唯美独秀 / 浪漫心形 / 星河旋涡)")
    print("   [ESC]   退出 / 切换全屏")
    print("   [空格]  暂停 / 继续 3D 旋转")
    print("   [D]     立即触发花瓣解离扩散与倒流聚合")
    print("   [S]     暂停 / 继续左侧源码自动滚动")
    print("   [B]     开启 / 关闭 3D 全息线框立方体")
    print("   [T]     开启 / 关闭 左侧源码面板")
    print("   [H]     纯净沉浸模式 (隐藏底部提示文字)")
    print("   [Q]     安全退出程序")
    print("=" * 65)

    app = FullscreenRoseApp()
    app.root.mainloop()
'''

with open('particle_rose_3d.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated particle_rose_3d.py with 7 themes and 4 styles!')

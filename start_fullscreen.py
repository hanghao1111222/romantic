#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌹 粒子玫瑰 · 本地原生独立全屏启动器 (无浏览器地址栏/标签页干扰)
- 以独立桌面 WebApp 极简全屏模式启动粒子玫瑰
- 包含左侧原版 Python 源码自动平滑滚动系统
- 包含右侧 3D 全息线框立方体与高精三维粒子玫瑰盛宴
"""

import subprocess
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(DIR, "particle_rose_fullscreen.html")

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE_BIN = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

def main():
    target_bin = None
    if os.path.exists(CHROME_BIN):
        target_bin = CHROME_BIN
    elif os.path.exists(EDGE_BIN):
        target_bin = EDGE_BIN

    print("=" * 65)
    print("🌹 正在本地启动独立全屏模式 3D 粒子玫瑰 (原版代码自动滚动)...")
    print("💡 快捷键操作:")
    print("   [空格] 暂停/继续旋转 | [S] 暂停/恢复代码滚动 | [B] 3D线框开关")
    print("   [C]    左侧源码面板开关 | [F / F11] 切换全屏 | [H] 纯净录屏模式")
    print("   [ESC]  退出全屏")
    print("=" * 65)

    if target_bin:
        # 使用 --app 模式独立启动应用窗口（彻底去除浏览器 URL 栏、标签栏、导航栏，纯净全屏）
        subprocess.Popen([
            target_bin,
            f"--app=file://{HTML_PATH}",
            "--start-fullscreen",
            "--hide-scrollbars"
        ])
    else:
        # 系统默认备用打开
        os.system(f'open "file://{HTML_PATH}"')

if __name__ == "__main__":
    main()

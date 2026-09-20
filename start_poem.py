#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌹 Roses given, fragrance in hand. (赠人玫瑰，手有余香)
全屏沉浸手写诗启动器
"""
import subprocess
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(DIR, "roses.html")

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE_BIN = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

def main():
    target_bin = None
    if os.path.exists(CHROME_BIN):
        target_bin = CHROME_BIN
    elif os.path.exists(EDGE_BIN):
        target_bin = EDGE_BIN

    print("=" * 65)
    print("🌹 正在本地启动全屏手写诗: Roses given, fragrance in hand...")
    print("💡 互动说明:")
    print("   - 观赏英文字体行云流水的挥毫书写动画与星尘笔触")
    print("   - 点击屏幕任意位置可洒落飘飞玫瑰花瓣与璀璨星火")
    print("   - 点击「启奏余香心音」可聆听空灵纯净的纯代码合成琶音")
    print("   - 点击「探索 3D 粒子玫瑰实验室」可无缝过渡到 3D 粒子花朵世界")
    print("=" * 65)

    if target_bin:
        subprocess.Popen([
            target_bin,
            f"--app=file://{HTML_PATH}",
            "--start-fullscreen",
            "--hide-scrollbars"
        ])
    else:
        import webbrowser
        webbrowser.open(f"file://{HTML_PATH}")

if __name__ == "__main__":
    main()

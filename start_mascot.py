#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os

DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(DIR, "particle_mascot_studio.html")

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE_BIN = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

def main():
    target_bin = None
    if os.path.exists(CHROME_BIN):
        target_bin = CHROME_BIN
    elif os.path.exists(EDGE_BIN):
        target_bin = EDGE_BIN

    print("=" * 60)
    print("⚡ 正在启动 Particle Mascot Studio (粒子萌宠工作室)...")
    print("💡 交互操作:")
    print("   [鼠标按住拖拽]  3D 视差倾斜")
    print("   [点击画布]      粒子散开爆炸效果")
    print("   [右侧面板]      随时切换皮卡丘/蓝兔/粉猫/紫狐 4款角色及调节参数")
    print("=" * 60)

    if target_bin:
        subprocess.Popen([
            target_bin,
            f"--app=file://{HTML_PATH}",
            "--window-size=1300,920"
        ])
    else:
        os.system(f'open "file://{HTML_PATH}"')

if __name__ == "__main__":
    main()

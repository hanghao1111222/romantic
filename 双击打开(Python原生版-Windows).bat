@echo off
chcp 65001 >nul
title 3D 粒子玫瑰 · Python 原生全屏
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% equ 0 (
    python particle_rose_3d.py
    exit /b
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    py particle_rose_3d.py
    exit /b
)

echo 未检测到 Python 环境，正在为您自动打开 Web 极致渲染版本...
call "双击打开粒子玫瑰(Windows).bat"

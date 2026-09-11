@echo off
chcp 65001 >nul
title 3D 粒子玫瑰 · 全屏盛宴
cd /d "%~dp0"

echo =======================================================
echo  🌹 正在以独立全屏模式启动 3D 粒子玫瑰...
echo  💡 快捷键提示:
echo     [C] 换颜色主题  |  [V] 换花朵形态  |  [空格] 暂停旋转
echo     [S] 源码滚动开关 |  [B] 3D全息线框 |  [ESC] 退出全屏
echo =======================================================

set "HTML=%~dp0particle_rose_fullscreen.html"

:: 优先检测并使用 Chrome 独立 App 全屏模式 (无地址栏、无标签页)
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --app="file:///%HTML:\=/%" --start-fullscreen --hide-scrollbars
    exit /b
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --app="file:///%HTML:\=/%" --start-fullscreen --hide-scrollbars
    exit /b
)
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
    start "" "%LocalAppData%\Google\Chrome\Application\chrome.exe" --app="file:///%HTML:\=/%" --start-fullscreen --hide-scrollbars
    exit /b
)

:: 其次检测 Windows 10/11 自带的 Microsoft Edge 独立 App 全屏模式
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML:\=/%" --start-fullscreen --hide-scrollbars
    exit /b
)
if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
    start "" "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML:\=/%" --start-fullscreen --hide-scrollbars
    exit /b
)

:: 备用方式：直接调起系统默认浏览器打开
start "" "%HTML%"

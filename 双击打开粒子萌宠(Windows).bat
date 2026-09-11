@echo off
chcp 65001 > nul
set DIR=%~dp0
set HTML=%DIR%particle_mascot_studio.html

echo ======================================================
echo ⚡ 正在打开 Particle Mascot Studio 粒子萌宠工作室...
echo ======================================================

set CHROME="C:\Program Files\Google\Chrome\Application\chrome.exe"
set EDGE="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
set EDGE64="C:\Program Files\Microsoft\Edge\Application\msedge.exe"

if exist %CHROME% (
    start "" %CHROME% --app="file:///%HTML%" --window-size=1300,920
) else if exist %EDGE64% (
    start "" %EDGE64% --app="file:///%HTML%" --window-size=1300,920
) else if exist %EDGE% (
    start "" %EDGE% --app="file:///%HTML%" --window-size=1300,920
) else (
    start "" "file:///%HTML%"
)

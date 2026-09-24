@echo off
chcp 65001 >nul
cd /d "%~dp0"
python alimokhtar_tool.py
if errorlevel 1 pause
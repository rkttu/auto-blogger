@echo off
REM Auto-Blogger Wrapper Script for Windows (Command)
REM This script allows you to run auto-blogger from anywhere

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Remove trailing backslash
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Change to the project directory and run auto-blogger with all arguments
cd /d "%SCRIPT_DIR%" && uv run auto-blogger %*

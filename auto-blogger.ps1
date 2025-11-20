#!/usr/bin/env pwsh
# Auto-Blogger Wrapper Script for PowerShell
# This script allows you to run auto-blogger from anywhere

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to the project directory and run auto-blogger with all arguments
Push-Location $ScriptDir
try {
    uv run auto-blogger @args
} finally {
    Pop-Location
}

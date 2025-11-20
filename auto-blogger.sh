#!/bin/bash
# Auto-Blogger Wrapper Script for Linux/macOS
# This script allows you to run auto-blogger from anywhere

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory and run auto-blogger with all arguments
cd "$SCRIPT_DIR" && uv run auto-blogger "$@"

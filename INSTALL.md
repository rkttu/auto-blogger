# Auto-Blogger Installation Guide

This guide explains how to use auto-blogger from anywhere on your system using wrapper scripts.

## Prerequisites

- UV package manager installed
- Python 3.12+ installed
- Auto-blogger project cloned/downloaded

## Wrapper Scripts

- `auto-blogger.sh` - Linux/macOS (Bash)
- `auto-blogger.cmd` - Windows (Command Prompt)
- `auto-blogger.ps1` - Windows (PowerShell)

## Installation Methods

### Option 1: Add to PATH (Recommended)

#### Linux/macOS

1. Add the project directory to your PATH in `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

    ```bash
    export PATH="$PATH:/Users/rkttu/Projects/auto-blogger"
    ```

2. Reload your shell configuration:

    ```bash
    source ~/.bashrc  # or ~/.zshrc
    ```

3. Now you can run from anywhere:

    ```bash
    auto-blogger.sh generate "My Topic" --tone technical
    ```

#### Windows (PowerShell)

1. Add to PATH permanently:

    ```powershell
    $env:Path += ";C:\Users\YourName\Projects\auto-blogger"
    [Environment]::SetEnvironmentVariable("Path", $env:Path, "User")
    ```

2. Restart PowerShell

3. Run from anywhere:

    ```powershell
    auto-blogger.ps1 generate "My Topic" --tone technical
    ```

#### Windows (Command Prompt)

1. Add to PATH via System Properties:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit PATH and add: `C:\Users\YourName\Projects\auto-blogger`

2. Restart Command Prompt

3. Run from anywhere:

```cmd
auto-blogger.cmd generate "My Topic" --tone technical
```

### Option 2: Create Alias

#### Linux/macOS (Bash/Zsh)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias auto-blogger='/Users/rkttu/Projects/auto-blogger/auto-blogger.sh'
```

Reload:

```bash
source ~/.bashrc  # or ~/.zshrc
```

Usage:

```bash
auto-blogger generate "My Topic" --tone technical
```

#### PowerShell

Add to your PowerShell profile (`$PROFILE`):

```powershell
function auto-blogger { & "C:\Users\YourName\Projects\auto-blogger\auto-blogger.ps1" @args }
```

Reload:

```powershell
. $PROFILE
```

Usage:

```powershell
auto-blogger generate "My Topic" --tone technical
```

### Option 3: Symlink (Linux/macOS)

Create a symlink in a directory already in your PATH:

```bash
sudo ln -s /Users/rkttu/Projects/auto-blogger/auto-blogger.sh /usr/local/bin/auto-blogger
```

Usage:

```bash
auto-blogger generate "My Topic" --tone technical
```

## Verification

Test the installation:

```bash
# Linux/macOS
auto-blogger.sh --help
# or (if using alias/symlink)
auto-blogger --help

# Windows (PowerShell)
auto-blogger.ps1 --help

# Windows (Command Prompt)
auto-blogger.cmd --help
```

## Usage Examples

### Generate a blog post

```bash
auto-blogger generate "Kubernetes Best Practices" --tone technical --length long
```

### Generate with research

```bash
auto-blogger generate "Azure Functions Tutorial" --research --tone technical
```

### Generate with front matter

```bash
auto-blogger generate "Docker Tips" --use-front-matter --author "DevOps Team"
```

### Save to file

```bash
auto-blogger generate "Python Asyncio" -o output.md --tone technical
```

## Troubleshooting

### "command not found" error

- Make sure the script has execute permissions: `chmod +x auto-blogger.sh`
- Verify the PATH includes the script directory: `echo $PATH`
- Check that UV is installed: `uv --version`

### PowerShell execution policy error

Run PowerShell as Administrator and execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Script not working from other directories

- Verify the script uses absolute paths (wrapper scripts handle this automatically)
- Make sure you're using the wrapper script, not running `uv run auto-blogger` directly

## Uninstallation

Remove the PATH entry or alias from your shell configuration file, or delete the symlink if you created one.

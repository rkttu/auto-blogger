# Auto-Blogger

AI-powered blog post generator CLI tool with MCP integration, SEO optimization, and Unsplash images.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

> 🌟 **Generate high-quality, SEO-optimized blog posts with automatic research, keywords, and professional images!**

## ✨ Key Features

- 🤖 **LangChain-powered** blog post generation with customizable tone and length
- 🔍 **MCP (Model Context Protocol)** integration for automatic research from trusted sources
- 🎯 **SEO Optimization**: Auto-generates keywords, abstract, and URL-friendly slugs
- 📸 **Unsplash Integration**: Automatically adds professional header images with proper attribution
- 📝 **YAML Front Matter**: Includes metadata (title, date, author, keywords, abstract)
- 🌍 **Multi-language Support**: Korean, English, and more
- 🔌 **OpenAI-compatible APIs**: Works with Azure OpenAI, OpenRouter, vLLM, LiteLLM, etc.
- 💻 **Cross-platform**: Wrapper scripts for Linux, macOS, and Windows
- 🎨 **Markdown Linter Compliant**: Clean, properly formatted markdown output

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Features in Detail](#features-in-detail)
- [Support This Project](#-support-this-project)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- UV package manager
- OpenAI API key (or compatible service)

### Installation

```bash
# Clone the repository
git clone https://github.com/rkttu/auto-blogger.git
cd auto-blogger

# Install dependencies with UV
uv sync

# Initialize configuration
uv run auto-blogger init
```

### Basic Usage

```bash
# Generate a blog post (default: 1 Unsplash image, Korean)
uv run auto-blogger generate "Your Topic Here"

# Save to file with custom options
uv run auto-blogger generate "AI in 2024" \
  --output ai-trends.md \
  --language English \
  --length long \
  --research
```

## ⚙️ Configuration

1. **Initialize configuration**:

    ```bash
    uv run auto-blogger init
    ```

2. **Edit `.env` file** with your credentials:

    ```bash
    # OpenAI Configuration
    OPENAI_API_KEY=your-api-key-here
    DEFAULT_MODEL=gpt-4o-mini
    OPENAI_API_BASE=  # Optional: for Azure OpenAI or compatible services

    # Blog Settings
    DEFAULT_LANGUAGE=Korean
    DEFAULT_TONE=professional
    DEFAULT_LENGTH=medium
    TEMPERATURE=0.7

    # MCP Servers (optional, for research)
    MCP_SERVERS=https://learn.microsoft.com/api/mcp

    # Unsplash API (optional, for images)
    UNSPLASH_APPLICATION_ID=your-app-id
    UNSPLASH_ACCESS_KEY=your-access-key
    UNSPLASH_SECRET_KEY=your-secret-key
    ```

## 📖 Usage Examples

### Generate with Images

```bash
# With 1 image (default)
uv run auto-blogger generate "Docker Best Practices"

# With multiple images
uv run auto-blogger generate "Cloud Architecture" --image-count 2

# Without images
uv run auto-blogger generate "API Design" --image-count 0
```

### Research Mode

```bash
# Gather reference materials from MCP servers
uv run auto-blogger generate "Kubernetes Security" \
  --research \
  --tone technical \
  --output k8s-security.md
```

### Multi-language Support

```bash
# Korean (default)
uv run auto-blogger generate "인공지능의 미래"

# English
uv run auto-blogger generate "The Future of AI" --language English
```

### Custom Tone and Length

```bash
# Technical, long-form article
uv run auto-blogger generate "Distributed Systems" \
  --tone technical \
  --length long

# Casual, short post
uv run auto-blogger generate "Weekend Coding Projects" \
  --tone casual \
  --length short
```

### CLI Options

```bash
Options:
  --output, -o PATH       Output file path (default: stdout)
  --language, -l TEXT     Language (default: Korean)
  --tone, -t TEXT         Tone: professional, casual, technical
  --length TEXT           Length: short (300-500), medium (800-1200), long (1500-2500)
  --research, -r          Enable MCP research
  --author, -a TEXT       Author name (default: Auto-Blogger)
  --image-count, -i INT   Number of images (0-3, default: 1)
  --help                  Show help message
```

## 🎯 Features in Detail

### SEO Optimization

Auto-Blogger automatically generates:

- **Keywords**: 5-8 relevant SEO keywords extracted from content
- **Abstract**: 2-3 sentence marketing-friendly summary
- **URL Slug**: English-friendly slug (even for non-English titles)

### MCP Integration

Leverage Model Context Protocol servers for research:

- Microsoft Learn documentation
- Custom MCP servers
- Automatic reference gathering and citation

### Unsplash Images

Professional images with:

- Keyword-based search
- Proper attribution (required by Unsplash)
- Download tracking (API compliance)
- Markdown-ready formatting

### Output Format

```markdown
---
title: "Your Title"
date: 2024-11-20
author: Auto-Blogger
language: English
slug: your-title-slug
keywords:
  - keyword1
  - keyword2
abstract: |
  Your auto-generated abstract here.
---

![Photo by Photographer on Unsplash](image-url)

*Photo by [Photographer](link) on [Unsplash](link)*

> This article was written with partial assistance from generative AI.

# Your Title

[Content here...]
```

## 💖 Support This Project

If Auto-Blogger helps you create better content faster, please consider:

- ⭐ **Star this repository** on GitHub
- 🐛 **Report issues** or suggest new features
- 🔀 **Contribute** via pull requests
- 💝 **Sponsor** via [GitHub Sponsors](https://github.com/sponsors/rkttu)

Your support helps maintain and improve this project. Every contribution, big or small, makes a difference!

## 🛠️ Development️ Development

```bash
# Install dependencies
uv sync

# Run locally
uv run auto-blogger generate "Test Topic"

# Run tests (if available)
uv run pytest
```

## 🗺️ Roadmap

- [x] LangChain integration
- [x] MCP server support for research
- [x] SEO optimization (keywords, abstract, slug)
- [x] Unsplash image integration
- [x] YAML front matter
- [x] OpenAI-compatible API support
- [x] Cross-platform wrapper scripts
- [ ] LlamaIndex integration for advanced RAG
- [ ] Multiple MCP servers simultaneously
- [ ] Batch post generation
- [ ] Platform-specific optimizations (Dev.to, Medium, WordPress)
- [ ] WebSocket-based MCP servers
- [ ] Web UI (optional)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Images from [Unsplash](https://unsplash.com)
- Research powered by [Model Context Protocol](https://modelcontextprotocol.io)

---

**Made with ❤️ by [rkttu](https://github.com/rkttu)**

If this project helps you, please consider [sponsoring](https://github.com/sponsors/rkttu) ⭐

"""Configuration management for auto-blogger."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration for the blog generator."""
    
    openai_api_key: str
    model: str = "gpt-4o-mini"
    default_language: str = "Korean"
    default_tone: str = "professional"
    default_length: str = "medium"
    temperature: float = 0.7
    mcp_servers: list[str] = None
    openai_api_base: Optional[str] = None
    
    def __post_init__(self):
        """Initialize mcp_servers if None."""
        if self.mcp_servers is None:
            self.mcp_servers = []
    
    @classmethod
    def load(cls, env_path: Optional[Path] = None) -> "Config":
        """Load configuration from environment variables and .env file."""
        if env_path is None:
            env_path = Path(".env")
        
        if env_path.exists():
            load_dotenv(env_path)
        
        # Parse MCP servers from environment
        mcp_servers_str = os.getenv("MCP_SERVERS", "")
        mcp_servers = [s.strip() for s in mcp_servers_str.split(",") if s.strip()]
        
        # Get OpenAI API base URL (for compatible services)
        api_base = os.getenv("OPENAI_API_BASE", None)
        if api_base and not api_base.strip():
            api_base = None
        
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("DEFAULT_MODEL", "gpt-4o-mini"),
            default_language=os.getenv("DEFAULT_LANGUAGE", "Korean"),
            default_tone=os.getenv("DEFAULT_TONE", "professional"),
            default_length=os.getenv("DEFAULT_LENGTH", "medium"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            mcp_servers=mcp_servers,
            openai_api_base=api_base,
        )

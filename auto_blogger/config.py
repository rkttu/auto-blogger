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
    
    # Unsplash configuration
    unsplash_application_id: Optional[str] = None
    unsplash_access_key: Optional[str] = None
    unsplash_secret_key: Optional[str] = None
    
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
        
        # Get Unsplash credentials (optional)
        unsplash_app_id = os.getenv("UNSPLASH_APPLICATION_ID", None)
        unsplash_access = os.getenv("UNSPLASH_ACCESS_KEY", None)
        unsplash_secret = os.getenv("UNSPLASH_SECRET_KEY", None)
        
        # Clean up empty strings
        if unsplash_app_id and not unsplash_app_id.strip():
            unsplash_app_id = None
        if unsplash_access and not unsplash_access.strip():
            unsplash_access = None
        if unsplash_secret and not unsplash_secret.strip():
            unsplash_secret = None
        
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("DEFAULT_MODEL", "gpt-4o-mini"),
            default_language=os.getenv("DEFAULT_LANGUAGE", "Korean"),
            default_tone=os.getenv("DEFAULT_TONE", "professional"),
            default_length=os.getenv("DEFAULT_LENGTH", "medium"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            mcp_servers=mcp_servers,
            openai_api_base=api_base,
            unsplash_application_id=unsplash_app_id,
            unsplash_access_key=unsplash_access,
            unsplash_secret_key=unsplash_secret,
        )

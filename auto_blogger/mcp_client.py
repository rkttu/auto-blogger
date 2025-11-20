"""MCP client for research and reference gathering."""

import asyncio
from typing import List, Dict, Any, Optional
import httpx
from contextlib import asynccontextmanager
import json


class MCPClient:
    """Simple HTTP-based client for MCP-compatible servers."""
    
    def __init__(self, server_url: str, timeout: int = 30):
        """Initialize MCP client with server URL."""
        self.server_url = server_url.rstrip('/')
        self.timeout = timeout
        self.http_client: Optional[httpx.AsyncClient] = None
        self.session_initialized = False
    
    @asynccontextmanager
    async def connect(self):
        """Connect to MCP server via HTTP."""
        async with httpx.AsyncClient(
            timeout=self.timeout, 
            follow_redirects=True,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        ) as http_client:
            try:
                self.http_client = http_client
                # Initialize session with MCP server
                await self._initialize_session()
                yield self
            finally:
                self.http_client = None
                self.session_initialized = False
    
    async def _initialize_session(self) -> bool:
        """Initialize MCP session with the server."""
        if not self.http_client:
            return False
        
        try:
            response = await self.http_client.post(
                self.server_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "auto-blogger",
                            "version": "0.1.0"
                        }
                    }
                }
            )
            response.raise_for_status()
            
            # Parse SSE (Server-Sent Events) format
            text = response.text
            result_data = self._parse_sse_response(text)
            
            if result_data and "result" in result_data:
                self.session_initialized = True
                print(f"MCP session initialized with {self.server_url}")
                server_info = result_data.get("result", {}).get("serverInfo", {})
                print(f"Server: {server_info.get('name', 'Unknown')} v{server_info.get('version', 'Unknown')}")
                return True
            
            return False
        except Exception as e:
            print(f"Warning: Could not initialize MCP session: {e}")
            return False
    
    def _parse_sse_response(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse Server-Sent Events format response."""
        try:
            lines = text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    data_str = line[6:]  # Remove 'data: ' prefix
                    return json.loads(data_str)
            return None
        except Exception as e:
            print(f"Error parsing SSE response: {e}")
            return None
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the MCP server."""
        if not self.http_client or not self.session_initialized:
            return []
        
        try:
            response = await self.http_client.post(
                self.server_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list"
                }
            )
            response.raise_for_status()
            
            # Parse SSE response
            result_data = self._parse_sse_response(response.text)
            tools = result_data.get("result", {}).get("tools", []) if result_data else []
            
            if tools:
                print(f"Available tools: {[t.get('name', 'unknown') for t in tools]}")
            return tools
        except Exception as e:
            print(f"Warning: Could not list tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool on the MCP server."""
        if not self.http_client or not self.session_initialized:
            return {"error": "Session not initialized"}
        
        try:
            response = await self.http_client.post(
                self.server_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                }
            )
            response.raise_for_status()
            
            # Parse SSE response
            result_data = self._parse_sse_response(response.text)
            return result_data.get("result", {}) if result_data else {"error": "No result"}
            
        except httpx.HTTPStatusError as e:
            print(f"Error calling tool {tool_name}: HTTP {e.response.status_code}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def search_content(self, query: str, tool_name: str = "microsoft_docs_search") -> str:
        """Search for content related to the query."""
        result = await self.call_tool(tool_name, {"query": query})
        
        # Handle error responses
        if "error" in result:
            return ""
        
        # Extract text content from the result
        if "content" in result:
            content_list = result["content"]
            if isinstance(content_list, list):
                texts = []
                for item in content_list:
                    if isinstance(item, dict):
                        # Handle text type content
                        if item.get("type") == "text":
                            texts.append(item.get("text", ""))
                        # Handle resource type content
                        elif "text" in item:
                            texts.append(item["text"])
                return "\n\n".join(texts)
            return str(content_list)
        
        return ""


class ResearchHelper:
    """Helper class to gather research materials for blog posts."""
    
    def __init__(self, mcp_servers: List[str]):
        """Initialize with list of MCP server URLs."""
        self.mcp_servers = mcp_servers
    
    async def gather_references(self, topic: str, max_sources: int = 3) -> List[str]:
        """Gather reference materials from MCP servers."""
        references = []
        
        for server_url in self.mcp_servers[:max_sources]:
            try:
                print(f"Attempting to gather references from: {server_url}")
                client = MCPClient(server_url)
                async with client.connect():
                    # First, try to list available tools
                    tools = await client.list_tools()
                    if tools:
                        # Use microsoft_docs_search if available
                        tool_names = [t.get("name") for t in tools]
                        if "microsoft_docs_search" in tool_names:
                            content = await client.search_content(topic, "microsoft_docs_search")
                            if content and content.strip():
                                references.append(content)
                                continue
                        
                        # Otherwise use the first available tool
                        tool_name = tools[0].get("name", "search")
                        content = await client.search_content(topic, tool_name)
                        if content and content.strip():
                            references.append(content)
                            continue
                    
                    # If no tools listed, try common tool names
                    for tool_name in ["microsoft_docs_search", "search", "query", "get_content"]:
                        content = await client.search_content(topic, tool_name)
                        if content and content.strip():
                            references.append(content)
                            break
            except Exception as e:
                print(f"Warning: Could not gather from {server_url}: {e}")
                continue
        
        if not references:
            print("No references gathered from MCP servers. Continuing without research data.")
        
        return references
    
    def format_references(self, references: List[str]) -> str:
        """Format references for inclusion in prompts."""
        if not references:
            return ""
        
        formatted = "\n\n## Reference Materials:\n\n"
        for i, ref in enumerate(references, 1):
            formatted += f"### Source {i}\n{ref}\n\n"
        
        return formatted


def run_async_research(mcp_servers: List[str], topic: str) -> List[str]:
    """Synchronous wrapper for async research gathering."""
    helper = ResearchHelper(mcp_servers)
    return asyncio.run(helper.gather_references(topic))

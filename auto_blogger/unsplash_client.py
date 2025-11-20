"""Unsplash API client for fetching blog post images."""

import httpx
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class UnsplashImage:
    """Represents an image from Unsplash."""
    id: str
    url: str
    download_url: str
    description: str
    alt_description: str
    photographer_name: str
    photographer_url: str
    unsplash_url: str
    width: int
    height: int


class UnsplashClient:
    """Client for interacting with Unsplash API."""
    
    BASE_URL = "https://api.unsplash.com"
    
    def __init__(self, application_id: str, access_key: str, secret_key: str):
        """Initialize Unsplash client with credentials.
        
        Args:
            application_id: Unsplash Application ID
            access_key: Unsplash Access Key
            secret_key: Unsplash Secret Key
        """
        self.application_id = application_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = httpx.Client(
            headers={
                "Authorization": f"Client-ID {access_key}",
                "Accept-Version": "v1"
            }
        )
    
    def search_photos(self, query: str, per_page: int = 5, orientation: str = "landscape") -> List[UnsplashImage]:
        """Search for photos on Unsplash.
        
        Args:
            query: Search query (keywords)
            per_page: Number of results (max 30)
            orientation: Photo orientation (landscape, portrait, squarish)
            
        Returns:
            List of UnsplashImage objects
        """
        try:
            response = self.client.get(
                f"{self.BASE_URL}/search/photos",
                params={
                    "query": query,
                    "per_page": min(per_page, 30),
                    "orientation": orientation
                }
            )
            response.raise_for_status()
            data = response.json()
            
            images = []
            for result in data.get("results", []):
                images.append(UnsplashImage(
                    id=result["id"],
                    url=result["urls"]["regular"],
                    download_url=result["links"]["download_location"],
                    description=result.get("description") or result.get("alt_description") or "",
                    alt_description=result.get("alt_description") or result.get("description") or query,
                    photographer_name=result["user"]["name"],
                    photographer_url=result["user"]["links"]["html"],
                    unsplash_url=result["links"]["html"],
                    width=result["width"],
                    height=result["height"]
                ))
            
            return images
        
        except Exception as e:
            print(f"Error searching Unsplash: {e}")
            return []
    
    def trigger_download(self, download_url: str) -> bool:
        """Trigger download tracking for Unsplash attribution.
        
        This is required by Unsplash API guidelines to track image usage.
        
        Args:
            download_url: The download_location URL from the photo object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.get(download_url)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Warning: Could not trigger Unsplash download tracking: {e}")
            return False
    
    def format_markdown_image(self, image: UnsplashImage, trigger_download: bool = True) -> str:
        """Format an Unsplash image as Markdown with proper attribution.
        
        Args:
            image: UnsplashImage object
            trigger_download: Whether to trigger download tracking (required by API)
            
        Returns:
            Markdown formatted image with credit
        """
        if trigger_download:
            self.trigger_download(image.download_url)
        
        # Create markdown image with alt text
        markdown = f"![{image.alt_description}]({image.url})\n\n"
        
        # Add attribution as required by Unsplash guidelines
        markdown += f"*Photo by [{image.photographer_name}]({image.photographer_url}) on [Unsplash]({image.unsplash_url})*\n"
        
        return markdown
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

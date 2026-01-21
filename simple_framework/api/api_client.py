"""Simple API Client"""

import requests
from typing import Dict, Any, Optional


class APIClient:
    """HTTP client for API testing"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params, timeout=self.timeout)
    
    def post(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=json, timeout=self.timeout, **kwargs)
    
    def put(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, json=json, timeout=self.timeout, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, timeout=self.timeout, **kwargs)
    
    def set_auth_token(self, token: str):
        """Set authorization token"""
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def close(self):
        """Close session"""
        self.session.close()

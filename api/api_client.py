"""
API Client

Base HTTP client for backend interactions.

Responsibilities:
- Manage HTTP sessions
- Handle retries with exponential backoff
- Set common headers
- Serialize/deserialize requests/responses
- Error handling and logging
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """
    Base HTTP client with retry logic and common utilities.
    
    This client provides a foundation for all API interactions.
    """
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        retry_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API (e.g., https://api.example.com)
            timeout: Default timeout for requests in seconds
            retry_config: Retry configuration dict with:
                - max_attempts
                - backoff_factor
                - retry_on_status_codes
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure retries
        if retry_config:
            self._configure_retries(retry_config)
        
        # Default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
    
    def _configure_retries(self, config: Dict[str, Any]) -> None:
        """Configure retry strategy for the session"""
        max_attempts = config.get("max_attempts", 3)
        backoff_factor = config.get("backoff_factor", 2)
        status_forcelist = config.get("retry_on_status_codes", [500, 502, 503, 504])
        
        retry_strategy = Retry(
            total=max_attempts,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """
        Set authentication token in headers.
        
        Args:
            token: Auth token value
            token_type: Token type (Bearer, Basic, etc.)
        """
        self.session.headers.update({
            "Authorization": f"{token_type} {token}"
        })
    
    def set_header(self, key: str, value: str) -> None:
        """Set custom header"""
        self.session.headers.update({key: value})
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Send GET request.
        
        Args:
            endpoint: API endpoint (e.g., /users/123)
            params: Query parameters
            **kwargs: Additional requests parameters
        
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        
        response = self.session.get(
            url,
            params=params,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> requests.Response:
        """
        Send POST request.
        
        Args:
            endpoint: API endpoint
            json: JSON payload
            data: Form data
            **kwargs: Additional requests parameters
        
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        
        response = self.session.post(
            url,
            json=json,
            data=data,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Send PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        
        response = self.session.put(
            url,
            json=json,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """Send DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        
        response = self.session.delete(
            url,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Send PATCH request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url}")
        
        response = self.session.patch(
            url,
            json=json,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs
        )
        
        self._log_response(response)
        return response
    
    def _log_response(self, response: requests.Response) -> None:
        """Log response details"""
        logger.info(f"Response: {response.status_code}")
        
        if response.status_code >= 400:
            logger.error(f"Error response body: {response.text}")
    
    def close(self) -> None:
        """Close the session"""
        self.session.close()

"""
Authentication API

Backend authentication endpoints.

Responsibilities:
- Login via API
- Token refresh
- Logout
- Return auth tokens/cookies
"""

from api.api_client import APIClient
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class AuthAPI:
    """
    Authentication API endpoints.
    
    This class encapsulates all auth-related backend operations.
    """
    
    def __init__(self, client: APIClient):
        """
        Initialize AuthAPI.
        
        Args:
            client: APIClient instance
        """
        self.client = client
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login via API.
        
        Args:
            username: Username or email
            password: Password
        
        Returns:
            Dict containing auth response (tokens, user info, etc.)
        
        Raises:
            Exception: If login fails
        """
        payload = {
            "username": username,
            "password": password
        }
        
        logger.info(f"Attempting API login for user: {username}")
        
        response = self.client.post("/auth/login", json=payload)
        
        if response.status_code == 200:
            auth_data = response.json()
            logger.info(f"Login successful for user: {username}")
            return auth_data
        else:
            logger.error(f"Login failed: {response.status_code} - {response.text}")
            raise Exception(f"Login failed with status {response.status_code}")
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh authentication token.
        
        Args:
            refresh_token: Refresh token
        
        Returns:
            Dict containing new auth tokens
        """
        payload = {
            "refresh_token": refresh_token
        }
        
        logger.info("Refreshing authentication token")
        
        response = self.client.post("/auth/refresh", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token refresh failed with status {response.status_code}")
    
    def logout(self, token: str) -> bool:
        """
        Logout and invalidate token.
        
        Args:
            token: Auth token to invalidate
        
        Returns:
            True if logout successful
        """
        # Set token for this request
        original_auth = self.client.session.headers.get("Authorization")
        self.client.set_auth_token(token)
        
        logger.info("Logging out")
        
        response = self.client.post("/auth/logout")
        
        # Restore original auth
        if original_auth:
            self.client.session.headers["Authorization"] = original_auth
        else:
            self.client.session.headers.pop("Authorization", None)
        
        return response.status_code == 200
    
    def validate_token(self, token: str) -> bool:
        """
        Validate if token is still valid.
        
        Args:
            token: Auth token to validate
        
        Returns:
            True if token is valid
        """
        # Set token for this request
        original_auth = self.client.session.headers.get("Authorization")
        self.client.set_auth_token(token)
        
        logger.info("Validating token")
        
        try:
            response = self.client.get("/auth/validate")
            valid = response.status_code == 200
        except Exception:
            valid = False
        finally:
            # Restore original auth
            if original_auth:
                self.client.session.headers["Authorization"] = original_auth
            else:
                self.client.session.headers.pop("Authorization", None)
        
        return valid

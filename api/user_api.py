"""
User API

User-related backend operations.

Responsibilities:
- CRUD operations for users
- User search and listing
- Return structured responses
"""

from api.api_client import APIClient
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class UserAPI:
    """
    User API endpoints.
    
    This class encapsulates all user-related backend operations.
    """
    
    def __init__(self, client: APIClient):
        """
        Initialize UserAPI.
        
        Args:
            client: APIClient instance (should be authenticated)
        """
        self.client = client
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            user_data: Dict containing user information
                - email (required)
                - password (required)
                - name, role, etc. (optional)
        
        Returns:
            Dict containing created user data
        """
        logger.info(f"Creating user: {user_data.get('email')}")
        
        response = self.client.post("/users", json=user_data)
        
        if response.status_code in [200, 201]:
            created_user = response.json()
            logger.info(f"User created successfully: {created_user.get('id')}")
            return created_user
        else:
            logger.error(f"User creation failed: {response.status_code} - {response.text}")
            raise Exception(f"User creation failed with status {response.status_code}")
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            Dict containing user data
        """
        logger.info(f"Fetching user: {user_id}")
        
        response = self.client.get(f"/users/{user_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Get user failed with status {response.status_code}")
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.
        
        Args:
            email: User email
        
        Returns:
            Dict containing user data, or None if not found
        """
        logger.info(f"Fetching user by email: {email}")
        
        response = self.client.get(f"/users", params={"email": email})
        
        if response.status_code == 200:
            users = response.json()
            return users[0] if users else None
        else:
            return None
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user.
        
        Args:
            user_id: User ID
            update_data: Dict containing fields to update
        
        Returns:
            Dict containing updated user data
        """
        logger.info(f"Updating user: {user_id}")
        
        response = self.client.put(f"/users/{user_id}", json=update_data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"User update failed with status {response.status_code}")
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user.
        
        Args:
            user_id: User ID
        
        Returns:
            True if deletion successful
        """
        logger.info(f"Deleting user: {user_id}")
        
        response = self.client.delete(f"/users/{user_id}")
        
        return response.status_code in [200, 204]
    
    def list_users(
        self,
        limit: int = 50,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List users with pagination and filters.
        
        Args:
            limit: Maximum number of users to return
            offset: Offset for pagination
            filters: Optional filters (role, status, etc.)
        
        Returns:
            List of user dicts
        """
        params = {
            "limit": limit,
            "offset": offset
        }
        
        if filters:
            params.update(filters)
        
        logger.info(f"Listing users with params: {params}")
        
        response = self.client.get("/users", params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"List users failed with status {response.status_code}")

"""
Authentication Manager

Handles authentication mechanics.

Responsibilities:
- Authenticate via UI or API
- Generate and persist storage state
- Validate if existing auth is still valid

Does NOT:
- Control authentication lifecycle (when to auth)
- Decide auth strategy (that's orchestrated by fixtures)
"""

from playwright.sync_api import Page, BrowserContext
from pathlib import Path
from typing import Dict, Any, Optional
import json
import time


class AuthManager:
    """
    Manages authentication mechanics.
    
    This class knows HOW to authenticate, but does NOT
    decide WHEN to authenticate (that's controlled by fixtures).
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize auth manager.
        
        Args:
            config: Configuration containing:
                - storage_state_path: Path to persist auth state
                - token_validity_seconds: How long tokens are valid
        """
        self.storage_state_path = Path(config.get(
            "storage_state_path",
            "auth_state/storage_state.json"
        ))
        self.token_validity_seconds = config.get("token_validity_seconds", 3600)
        
        # Ensure auth_state directory exists
        self.storage_state_path.parent.mkdir(parents=True, exist_ok=True)
    
    def authenticate_via_ui(
        self,
        page: Page,
        login_url: str,
        credentials: Dict[str, str]
    ) -> None:
        """
        Authenticate via UI and persist storage state.
        
        Args:
            page: Playwright Page instance
            login_url: URL to login page
            credentials: Dict with username/password
        """
        # Navigate to login page
        page.goto(login_url)
        
        # Perform login (this is a generic example)
        # In real implementation, this would use LoginPage from POM
        page.fill("input[name='username']", credentials["username"])
        page.fill("input[name='password']", credentials["password"])
        page.click("button[type='submit']")
        
        # Wait for navigation after login
        page.wait_for_load_state("networkidle")
        
        # Persist storage state
        self._save_storage_state(page.context)
    
    def authenticate_via_api(
        self,
        api_client,
        credentials: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Authenticate via API and return tokens.
        
        Args:
            api_client: API client instance
            credentials: Dict with username/password
        
        Returns:
            Dict containing auth tokens
        """
        # This is a placeholder - actual implementation depends on API
        response = api_client.post("/auth/login", json=credentials)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API authentication failed: {response.status_code}")
    
    def is_storage_state_valid(self) -> bool:
        """
        Check if existing storage state is valid.
        
        Returns:
            True if storage state exists and is not expired
        """
        if not self.storage_state_path.exists():
            return False
        
        # Check file age
        file_mtime = self.storage_state_path.stat().st_mtime
        current_time = time.time()
        age_seconds = current_time - file_mtime
        
        return age_seconds < self.token_validity_seconds
    
    def validate_auth_state(self, page: Page, validation_url: str) -> bool:
        """
        Validate authentication by attempting to access protected page.
        
        Args:
            page: Page with loaded storage state
            validation_url: URL of protected page to validate auth
        
        Returns:
            True if auth is valid, False otherwise
        """
        try:
            page.goto(validation_url, timeout=10000)
            
            # Check if we're still on the protected page (not redirected to login)
            # This is a simple check - real implementation might be more sophisticated
            return "/login" not in page.url.lower()
        except Exception:
            return False
    
    def _save_storage_state(self, context: BrowserContext) -> None:
        """
        Save current context storage state to file.
        
        Args:
            context: BrowserContext to save state from
        """
        context.storage_state(path=str(self.storage_state_path))
    
    def get_storage_state_path(self) -> Optional[str]:
        """
        Get path to storage state file if it exists and is valid.
        
        Returns:
            Path to storage state file, or None if invalid
        """
        if self.is_storage_state_valid():
            return str(self.storage_state_path)
        return None
    
    def clear_storage_state(self) -> None:
        """Remove stored authentication state"""
        if self.storage_state_path.exists():
            self.storage_state_path.unlink()

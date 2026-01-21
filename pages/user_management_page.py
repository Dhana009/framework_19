"""
User Management Page

Page Object for User Management page.

Encapsulates:
- User management locators
- User CRUD actions
- User list validations
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class UserManagementPage(BasePage):
    """
    User Management Page Object.
    
    Handles user creation, deletion, and management operations.
    """
    
    # ========================================================================
    # LOCATORS
    # ========================================================================
    
    CREATE_USER_BUTTON = "button:has-text('Create User'), button:has-text('Add User'), #create-user"
    USER_LIST_TABLE = ".user-table, table, .users-list"
    SEARCH_INPUT = "input[placeholder*='Search'], input[name='search']"
    
    # User form fields
    EMAIL_INPUT = "input[name='email'], #email"
    PASSWORD_INPUT = "input[name='password'], #password"
    NAME_INPUT = "input[name='name'], #name"
    ROLE_SELECT = "select[name='role'], #role"
    SAVE_BUTTON = "button[type='submit'], button:has-text('Save'), button:has-text('Create')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    
    # ========================================================================
    # ACTIONS
    # ========================================================================
    
    def __init__(self, page: Page, base_url: str):
        """
        Initialize User Management Page.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the application
        """
        super().__init__(page)
        self.base_url = base_url
        self.users_url = f"{base_url}/users"
    
    def goto(self) -> None:
        """Navigate to user management page"""
        self.navigate(self.users_url)
    
    def click_create_user(self) -> None:
        """Click create user button"""
        logger.info("Clicking create user button")
        self.click(self.CREATE_USER_BUTTON)
        self.wait_for_load_state("domcontentloaded")
    
    def create_user(self, user_data: Dict[str, Any]) -> None:
        """
        Create a new user via UI.
        
        Args:
            user_data: Dict containing user info:
                - email (required)
                - password (required)
                - name (optional)
                - role (optional)
        """
        logger.info(f"Creating user: {user_data.get('email')}")
        
        # Click create user button
        self.click_create_user()
        
        # Fill form
        self.fill(self.EMAIL_INPUT, user_data["email"])
        self.fill(self.PASSWORD_INPUT, user_data["password"])
        
        if "name" in user_data:
            self.fill(self.NAME_INPUT, user_data["name"])
        
        if "role" in user_data:
            self.select_option(self.ROLE_SELECT, user_data["role"])
        
        # Save
        self.click(self.SAVE_BUTTON)
        self.wait_for_load_state("networkidle")
    
    def search_user(self, email: str) -> None:
        """
        Search for user by email.
        
        Args:
            email: User email to search
        """
        logger.info(f"Searching for user: {email}")
        self.fill(self.SEARCH_INPUT, email)
        self.wait_for_load_state("networkidle")
    
    def delete_user(self, email: str) -> None:
        """
        Delete user by email.
        
        Args:
            email: User email to delete
        """
        logger.info(f"Deleting user: {email}")
        
        # Search for user
        self.search_user(email)
        
        # Click delete button (row-specific locator)
        delete_button = f"tr:has-text('{email}') button:has-text('Delete')"
        self.click(delete_button)
        
        # Confirm deletion if needed
        confirm_button = "button:has-text('Confirm'), button:has-text('Yes')"
        if self.is_visible(confirm_button, timeout=2000):
            self.click(confirm_button)
        
        self.wait_for_load_state("networkidle")
    
    # ========================================================================
    # VALIDATIONS
    # ========================================================================
    
    def is_loaded(self) -> bool:
        """
        Check if user management page is loaded.
        
        Returns:
            True if page is loaded
        """
        return self.is_visible(self.USER_LIST_TABLE, timeout=5000)
    
    def user_exists(self, email: str) -> bool:
        """
        Check if user exists in the list.
        
        Args:
            email: User email
        
        Returns:
            True if user is in the list
        """
        self.search_user(email)
        user_row = f"tr:has-text('{email}')"
        return self.is_visible(user_row, timeout=3000)

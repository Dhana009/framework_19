"""
Login Page

Page Object for Login page.

Encapsulates:
- Login page locators
- Login actions
- Login validation
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Login Page Object.
    
    Exposes business-level methods for login operations.
    """
    
    # ========================================================================
    # LOCATORS
    # ========================================================================
    
    USERNAME_INPUT = "input[name='username'], input[type='email'], #username, #email"
    PASSWORD_INPUT = "input[name='password'], input[type='password'], #password"
    LOGIN_BUTTON = "button[type='submit'], button:has-text('Login'), button:has-text('Sign In')"
    ERROR_MESSAGE = ".error-message, .alert-danger, [role='alert']"
    
    # ========================================================================
    # ACTIONS
    # ========================================================================
    
    def __init__(self, page: Page, base_url: str):
        """
        Initialize Login Page.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the application
        """
        super().__init__(page)
        self.base_url = base_url
        self.login_url = f"{base_url}/login"
    
    def goto(self) -> None:
        """Navigate to login page"""
        self.navigate(self.login_url)
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login.
        
        Args:
            username: Username or email
            password: Password
        """
        logger.info(f"Logging in as: {username}")
        
        # Fill credentials
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        
        # Click login
        self.click(self.LOGIN_BUTTON)
        
        # Wait for navigation
        self.wait_for_load_state("networkidle")
    
    # ========================================================================
    # VALIDATIONS
    # ========================================================================
    
    def is_login_successful(self) -> bool:
        """
        Check if login was successful.
        
        Returns:
            True if redirected away from login page
        """
        return "/login" not in self.url.lower()
    
    def get_error_message(self) -> str:
        """
        Get error message if login failed.
        
        Returns:
            Error message text
        """
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

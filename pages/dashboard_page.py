"""
Dashboard Page

Page Object for Dashboard/Home page.

Encapsulates:
- Dashboard locators
- Navigation actions
- Dashboard validations
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    """
    Dashboard Page Object.
    
    Represents the main dashboard/home page after login.
    """
    
    # ========================================================================
    # LOCATORS
    # ========================================================================
    
    WELCOME_MESSAGE = ".welcome-message, h1, .user-greeting"
    USER_MENU = ".user-menu, .profile-dropdown, #user-menu"
    USER_MANAGEMENT_LINK = "a:has-text('User Management'), a:has-text('Users')"
    LOGOUT_BUTTON = "button:has-text('Logout'), a:has-text('Logout')"
    
    # ========================================================================
    # ACTIONS
    # ========================================================================
    
    def __init__(self, page: Page, base_url: str):
        """
        Initialize Dashboard Page.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL of the application
        """
        super().__init__(page)
        self.base_url = base_url
        self.dashboard_url = f"{base_url}/dashboard"
    
    def goto(self) -> None:
        """Navigate to dashboard"""
        self.navigate(self.dashboard_url)
    
    def navigate_to_user_management(self) -> None:
        """Navigate to User Management page"""
        logger.info("Navigating to User Management")
        self.click(self.USER_MANAGEMENT_LINK)
        self.wait_for_load_state("networkidle")
    
    def logout(self) -> None:
        """Perform logout"""
        logger.info("Logging out")
        
        # Click user menu if exists
        if self.is_visible(self.USER_MENU, timeout=2000):
            self.click(self.USER_MENU)
        
        # Click logout
        self.click(self.LOGOUT_BUTTON)
        self.wait_for_load_state("networkidle")
    
    # ========================================================================
    # VALIDATIONS
    # ========================================================================
    
    def is_loaded(self) -> bool:
        """
        Check if dashboard is loaded.
        
        Returns:
            True if dashboard elements are visible
        """
        return self.is_visible(self.WELCOME_MESSAGE, timeout=5000)
    
    def get_welcome_message(self) -> str:
        """
        Get welcome message text.
        
        Returns:
            Welcome message text
        """
        if self.is_visible(self.WELCOME_MESSAGE):
            return self.get_text(self.WELCOME_MESSAGE)
        return ""

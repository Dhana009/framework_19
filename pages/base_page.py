"""
Base Page

Shared UI behavior for all page objects.

Responsibilities:
- Common waits and interactions
- Generic UI utilities
- Screenshot capture
- Error handling

Does NOT:
- Contain page-specific logic
- Know about test assertions
"""

from playwright.sync_api import Page, expect
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all Page Objects.
    
    Provides common utilities and interactions that all pages can use.
    """
    
    def __init__(self, page: Page):
        """
        Initialize base page.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
    
    # ========================================================================
    # NAVIGATION
    # ========================================================================
    
    def navigate(self, url: str, wait_until: str = "networkidle") -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
            wait_until: Wait condition (load, domcontentloaded, networkidle)
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until)
    
    def reload(self, wait_until: str = "networkidle") -> None:
        """Reload current page"""
        logger.info("Reloading page")
        self.page.reload(wait_until=wait_until)
    
    def go_back(self) -> None:
        """Navigate back"""
        self.page.go_back()
    
    # ========================================================================
    # ELEMENT INTERACTIONS
    # ========================================================================
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click element.
        
        Args:
            selector: CSS selector or text selector
            timeout: Optional timeout in milliseconds
        """
        logger.info(f"Clicking: {selector}")
        kwargs = {"timeout": timeout} if timeout else {}
        self.page.click(selector, **kwargs)
    
    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Fill input field.
        
        Args:
            selector: CSS selector
            text: Text to fill
            timeout: Optional timeout in milliseconds
        """
        logger.info(f"Filling '{selector}' with text")
        kwargs = {"timeout": timeout} if timeout else {}
        self.page.fill(selector, text, **kwargs)
    
    def select_option(self, selector: str, value: str) -> None:
        """Select option from dropdown"""
        logger.info(f"Selecting option: {value}")
        self.page.select_option(selector, value)
    
    def check(self, selector: str) -> None:
        """Check checkbox"""
        self.page.check(selector)
    
    def uncheck(self, selector: str) -> None:
        """Uncheck checkbox"""
        self.page.uncheck(selector)
    
    # ========================================================================
    # ELEMENT QUERIES
    # ========================================================================
    
    def get_text(self, selector: str) -> str:
        """Get element text content"""
        return self.page.text_content(selector) or ""
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get element attribute value"""
        return self.page.get_attribute(selector, attribute)
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def is_hidden(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is hidden"""
        try:
            self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
            return True
        except Exception:
            return False
    
    # ========================================================================
    # WAITS
    # ========================================================================
    
    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[int] = None
    ) -> None:
        """
        Wait for selector.
        
        Args:
            selector: CSS selector
            state: visible, hidden, attached, detached
            timeout: Optional timeout in milliseconds
        """
        logger.info(f"Waiting for selector: {selector} (state={state})")
        kwargs = {"timeout": timeout} if timeout else {}
        self.page.wait_for_selector(selector, state=state, **kwargs)
    
    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to match pattern"""
        logger.info(f"Waiting for URL: {url_pattern}")
        kwargs = {"timeout": timeout} if timeout else {}
        self.page.wait_for_url(url_pattern, **kwargs)
    
    def wait_for_load_state(self, state: str = "networkidle") -> None:
        """
        Wait for load state.
        
        Args:
            state: load, domcontentloaded, networkidle
        """
        self.page.wait_for_load_state(state)
    
    # ========================================================================
    # SCREENSHOTS
    # ========================================================================
    
    def screenshot(self, path: str, full_page: bool = False) -> None:
        """
        Take screenshot.
        
        Args:
            path: Path to save screenshot
            full_page: Capture full scrollable page
        """
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path, full_page=full_page)
    
    # ========================================================================
    # PAGE PROPERTIES
    # ========================================================================
    
    @property
    def url(self) -> str:
        """Get current URL"""
        return self.page.url
    
    @property
    def title(self) -> str:
        """Get page title"""
        return self.page.title()

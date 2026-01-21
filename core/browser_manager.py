"""
Browser Manager

Encapsulates browser launch logic.

Responsibilities:
- Launch browser with specified type and options
- Apply global browser-level settings
- Return Browser instance

Does NOT:
- Manage browser lifecycle (that's done by fixtures)
- Create contexts
- Handle authentication
"""

from playwright.sync_api import Browser, sync_playwright
from typing import Dict, Any, List


class BrowserManager:
    """
    Manages browser launch configuration and execution.
    
    This class knows HOW to launch a browser, but does NOT
    decide WHEN to launch it (that's controlled by fixtures).
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize browser manager with configuration.
        
        Args:
            config: Browser configuration dict containing:
                - type: Browser type (chromium, firefox, webkit)
                - headless: Run in headless mode
                - viewport: Viewport dimensions
                - slowmo: Slow motion delay
                - args: Additional browser arguments
        """
        self.browser_type = config.get("type", "chromium")
        self.headless = config.get("headless", False)
        self.viewport = config.get("viewport", {"width": 1920, "height": 1080})
        self.slowmo = config.get("slowmo", 0)
        self.args = config.get("args", [])
    
    def launch(self, playwright) -> Browser:
        """
        Launch browser with configured settings.
        
        Args:
            playwright: Playwright instance from sync_playwright()
        
        Returns:
            Browser instance
        """
        # Select browser type
        if self.browser_type == "firefox":
            browser_type = playwright.firefox
        elif self.browser_type == "webkit":
            browser_type = playwright.webkit
        else:  # Default to chromium
            browser_type = playwright.chromium
        
        # Launch browser with configuration
        browser = browser_type.launch(
            headless=self.headless,
            slow_mo=self.slowmo,
            args=self.args,
        )
        
        return browser
    
    def get_browser_context_options(self) -> Dict[str, Any]:
        """
        Get default options for creating browser contexts.
        
        These options are applied when creating contexts.
        """
        return {
            "viewport": self.viewport,
            "ignore_https_errors": True,  # Useful for testing environments
            "locale": "en-US",
            "timezone_id": "America/New_York",
        }

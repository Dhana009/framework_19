"""
Context Manager

Creates isolated browser contexts.

Responsibilities:
- Create browser context with specified options
- Load storage state if provided (for auth)
- Ensure session isolation

Does NOT:
- Validate authentication
- Decide when contexts are created
- Manage context lifecycle
"""

from playwright.sync_api import Browser, BrowserContext
from typing import Dict, Any, Optional
from pathlib import Path


class ContextManager:
    """
    Manages browser context creation.
    
    This class knows HOW to create isolated contexts, but does NOT
    decide WHEN to create them (that's controlled by fixtures).
    """
    
    def __init__(self, browser: Browser, default_options: Dict[str, Any]):
        """
        Initialize context manager.
        
        Args:
            browser: Browser instance
            default_options: Default context options (viewport, etc.)
        """
        self.browser = browser
        self.default_options = default_options
    
    def create_context(
        self,
        storage_state: Optional[str] = None,
        **kwargs
    ) -> BrowserContext:
        """
        Create a new isolated browser context.
        
        Args:
            storage_state: Path to storage state file (for auth persistence)
            **kwargs: Additional context options to override defaults
        
        Returns:
            BrowserContext instance with isolated cookies/session
        """
        # Merge default options with provided options
        context_options = {**self.default_options, **kwargs}
        
        # Add storage state if provided and file exists
        if storage_state and Path(storage_state).exists():
            context_options["storage_state"] = storage_state
        
        # Create and return context
        context = self.browser.new_context(**context_options)
        
        return context
    
    def create_page_from_context(self, context: BrowserContext):
        """
        Create a new page from a context.
        
        Args:
            context: BrowserContext instance
        
        Returns:
            Page instance
        """
        return context.new_page()

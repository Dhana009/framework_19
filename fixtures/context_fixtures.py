"""
Context Fixtures

Controls context and page lifecycle per test.

Responsibilities:
- Create fresh context for each test
- Create page from context
- Ensure isolation
- Cleanup after test

Uses context_manager to create contexts.
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from core.context_manager import ContextManager


@pytest.fixture(scope="function")
def context_manager(browser, browser_manager):
    """
    Provide ContextManager instance.
    
    Scope: function (new manager for each test if needed)
    """
    default_options = browser_manager.get_browser_context_options()
    return ContextManager(browser, default_options)


@pytest.fixture(scope="function")
def context(context_manager, auth_state):
    """
    Create fresh browser context for each test.
    
    This fixture:
    - Requests authenticated storage state
    - Creates isolated context with auth
    - Yields context to test
    - Closes context after test
    
    Scope: function (new context per test ensures isolation)
    """
    # Get storage state path from auth fixture
    storage_state_path = auth_state
    
    # Create context with auth state
    ctx = context_manager.create_context(storage_state=storage_state_path)
    
    yield ctx
    
    # Cleanup
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    """
    Create page from context for each test.
    
    This fixture:
    - Creates new page from context
    - Yields page to test
    - Closes page after test
    
    Scope: function (new page per test)
    """
    page = context.new_page()
    
    yield page
    
    # Cleanup
    page.close()


@pytest.fixture(scope="function")
def unauthenticated_context(context_manager):
    """
    Create context WITHOUT authentication.
    
    Useful for login tests where we need to start unauthenticated.
    
    Scope: function
    """
    ctx = context_manager.create_context(storage_state=None)
    
    yield ctx
    
    ctx.close()


@pytest.fixture(scope="function")
def unauthenticated_page(unauthenticated_context):
    """
    Create page without authentication.
    
    Scope: function
    """
    page = unauthenticated_context.new_page()
    
    yield page
    
    page.close()


@pytest.fixture(scope="function")
def multi_browser_context(multi_browser, browser_manager):
    """
    Create context for multi-browser fixture.
    
    Works with multi_browser fixture for cross-browser testing.
    
    Usage:
        def test_something(multi_browser_context):
            page = multi_browser_context.new_page()
            page.goto("https://example.com")
    
    Scope: function (fresh context per test)
    """
    default_options = browser_manager.get_browser_context_options()
    ctx = multi_browser.new_context(**default_options)
    
    yield ctx
    
    ctx.close()


@pytest.fixture(scope="function")
def multi_browser_page(multi_browser_context):
    """
    Create page for multi-browser fixture.
    
    Works with multi_browser fixture for cross-browser testing.
    
    Usage:
        def test_something(multi_browser_page):
            multi_browser_page.goto("https://example.com")
            assert "Example" in multi_browser_page.title()
    
    Scope: function (fresh page per test)
    """
    page = multi_browser_context.new_page()
    
    yield page
    
    page.close()
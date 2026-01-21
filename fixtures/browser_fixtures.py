"""
Browser Fixtures

Controls browser lifecycle.

Responsibilities:
- Launch browser at session start
- Close browser at session end
- Provide browser instance to tests

Uses browser_manager to perform the actual launch.
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, Playwright
from core.browser_manager import BrowserManager
from config.config_loader import get_config


@pytest.fixture(scope="session")
def config(request):
    """
    Provide configuration to all tests.
    
    Scope: session (created once per test session)
    """
    return get_config(request)


@pytest.fixture(scope="session")
def playwright_instance():
    """
    Provide Playwright instance for the session.
    
    Scope: session
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser_manager(config):
    """
    Provide BrowserManager instance.
    
    Scope: session
    """
    browser_config = config.browser_config
    return BrowserManager(browser_config)


@pytest.fixture(scope="session")
def browser(playwright_instance, browser_manager):
    """
    Launch browser for the test session.
    
    This fixture:
    - Launches browser using browser_manager
    - Yields browser to tests
    - Closes browser after all tests complete
    
    Scope: session (one browser for all tests)
    """
    # Launch browser
    browser = browser_manager.launch(playwright_instance)
    
    print(f"\n{'='*60}")
    print(f"Browser launched: {browser_manager.browser_type}")
    print(f"Headless: {browser_manager.headless}")
    print(f"{'='*60}\n")
    
    yield browser
    
    # Cleanup
    browser.close()
    print("\nBrowser closed")


@pytest.fixture(params=["chromium", "firefox", "webkit"], scope="session")
def multi_browser(request, playwright_instance, browser_manager):
    """
    Parametrized fixture for multi-browser testing.
    
    Runs tests on all three browsers: chromium, firefox, webkit
    
    Usage:
        def test_something(multi_browser):
            page = multi_browser.new_context().new_page()
            page.goto("https://example.com")
    
    Run command: pytest -v
    Output: test runs 3 times (once per browser)
    
    Scope: session (one browser per parameter)
    """
    browser_type = request.param
    
    # Get the right browser type
    if browser_type == "firefox":
        playwright_browser_type = playwright_instance.firefox
    elif browser_type == "webkit":
        playwright_browser_type = playwright_instance.webkit
    else:  # chromium
        playwright_browser_type = playwright_instance.chromium
    
    # Launch browser
    browser = playwright_browser_type.launch(
        headless=browser_manager.headless,
        slow_mo=browser_manager.slowmo,
        args=browser_manager.args,
    )
    
    print(f"\n{'='*60}")
    print(f"Multi-browser test: {browser_type}")
    print(f"{'='*60}\n")
    
    yield browser
    
    # Cleanup
    browser.close()
    print(f"\nBrowser ({browser_type}) closed")
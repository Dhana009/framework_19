"""
Fixtures and Configuration

Controls:
- Browser launch/teardown
- Page creation
- API client creation
- Configuration loading
"""

import pytest
import yaml
from pathlib import Path
from playwright.sync_api import sync_playwright
from api.api_client import APIClient


# ============================================================================
# CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def pytest_addoption(parser):
    """Add command-line options"""
    parser.addoption(
        "--simple-browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser type: chromium, firefox, webkit"
    )
    parser.addoption(
        "--simple-headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


# ============================================================================
# BROWSER FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def playwright_instance():
    """Initialize Playwright"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(config, playwright_instance, request):
    """Launch browser (session scope - reused across tests)"""
    browser_type_name = request.config.getoption("--simple-browser")
    headless = request.config.getoption("--simple-headless")
    
    # Get browser launcher
    if browser_type_name == "firefox":
        browser_launcher = playwright_instance.firefox
    elif browser_type_name == "webkit":
        browser_launcher = playwright_instance.webkit
    else:
        browser_launcher = playwright_instance.chromium
    
    # Launch browser
    browser = browser_launcher.launch(
        headless=headless or config["browser"]["headless"],
        slow_mo=config["browser"]["slowmo"]
    )
    
    print(f"\n✓ Browser launched: {browser_type_name}")
    
    yield browser
    
    browser.close()
    print(f"✓ Browser closed")


@pytest.fixture(scope="function")
def context(browser, config):
    """Create context (fresh per test)"""
    context = browser.new_context(
        viewport=config["browser"]["viewport"]
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context, config):
    """Create page (fresh per test)"""
    page = context.new_page()
    page.set_default_timeout(config["ui"]["wait_timeout"])
    yield page
    page.close()


# ============================================================================
# API FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def api_client(config):
    """Create API client (session scope - reused)"""
    client = APIClient(
        base_url=config["api"]["base_url"],
        timeout=config["api"]["timeout"]
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def authenticated_api_client(api_client, config):
    """Create authenticated API client"""
    # In real scenario, authenticate and get token
    # For now, just return the client
    return api_client

"""
Root conftest.py - Orchestration Layer

This is the central orchestration layer that:
- Registers all fixture modules
- Defines global hooks
- Adds custom CLI options
- Configures global test behavior

This file does NOT create browsers, contexts, or perform setup.
It only wires together the framework components.
"""

import pytest
from pathlib import Path

# ============================================================================
# FIXTURE PLUGIN REGISTRATION
# ============================================================================
# Register all fixture modules to make them available to tests

pytest_plugins = [
    "fixtures.browser_fixtures",
    "fixtures.context_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.api_fixtures",
    "fixtures.data_fixtures",
]


# ============================================================================
# CLI CUSTOM OPTIONS
# ============================================================================

def pytest_addoption(parser):
    """Add custom command-line options"""
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against: qa, staging, production",
        choices=["qa", "staging", "production"]
    )
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        help="Browser type: chromium, firefox, webkit",
        choices=["chromium", "firefox", "webkit"]
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


# ============================================================================
# GLOBAL HOOKS
# ============================================================================

def pytest_configure(config):
    """
    Called after command line options have been parsed.
    This is where global configuration is set up.
    """
    # Ensure reports directory exists
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    (reports_dir / "allure-results").mkdir(exist_ok=True)
    (reports_dir / "html-report").mkdir(exist_ok=True)
    
    # Ensure auth_state directory exists
    auth_state_dir = Path("auth_state")
    auth_state_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Framework Configuration:")
    print(f"  Environment: {config.getoption('--env')}")
    print(f"  Browser: {config.getoption('--browser-type')}")
    print(f"  Headless: {config.getoption('--headless')}")
    print(f"{'='*80}\n")


def pytest_sessionstart(session):
    """Called after Session object has been created, before collecting tests"""
    print("Test session starting...")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished, right before returning exit status"""
    print(f"\nTest session finished with exit status: {exitstatus}")


def pytest_runtest_setup(item):
    """Called before each test execution"""
    # This hook can be used for per-test setup logging
    pass


def pytest_runtest_teardown(item, nextitem):
    """Called after each test execution"""
    # This hook can be used for per-test cleanup logging
    pass


# ============================================================================
# MARKERS & TEST COLLECTION HOOKS
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """
    Called after collection is completed.
    Can be used to modify test items (e.g., add markers dynamically)
    """
    for item in items:
        # Auto-add 'ui' marker to tests in pages-related test files
        if "test_login" in item.nodeid or "dashboard" in item.nodeid:
            item.add_marker(pytest.mark.ui)
        
        # Auto-add 'api' marker to API test files
        if "api" in str(item.fspath).lower():
            item.add_marker(pytest.mark.api)

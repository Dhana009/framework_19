"""
Assertion Helpers

Reusable assertion utilities for tests.

Responsibilities:
- Provide custom assertions
- Improve assertion readability
- Generate helpful error messages
"""

from playwright.sync_api import Page, expect, Response
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# API ASSERTIONS
# ============================================================================

def assert_status_code(response: Response, expected: int, message: str = None) -> None:
    """
    Assert API response status code.
    
    Args:
        response: requests.Response object
        expected: Expected status code
        message: Optional custom error message
    """
    actual = response.status_code
    
    if actual != expected:
        error_msg = message or f"Expected status {expected}, got {actual}"
        logger.error(f"{error_msg} - Response: {response.text}")
        raise AssertionError(error_msg)


def assert_response_contains(response: Response, key: str, message: str = None) -> None:
    """
    Assert response JSON contains key.
    
    Args:
        response: requests.Response object
        key: Key to check for
        message: Optional custom error message
    """
    try:
        data = response.json()
    except Exception:
        raise AssertionError("Response is not valid JSON")
    
    if key not in data:
        error_msg = message or f"Response does not contain key: {key}"
        logger.error(error_msg)
        raise AssertionError(error_msg)


def assert_response_value(
    response: Response,
    key: str,
    expected_value: Any,
    message: str = None
) -> None:
    """
    Assert response JSON key has expected value.
    
    Args:
        response: requests.Response object
        key: Key to check
        expected_value: Expected value
        message: Optional custom error message
    """
    try:
        data = response.json()
    except Exception:
        raise AssertionError("Response is not valid JSON")
    
    actual_value = data.get(key)
    
    if actual_value != expected_value:
        error_msg = message or f"Expected {key}={expected_value}, got {actual_value}"
        logger.error(error_msg)
        raise AssertionError(error_msg)


# ============================================================================
# UI ASSERTIONS
# ============================================================================

def assert_element_visible(page: Page, selector: str, timeout: int = 5000) -> None:
    """
    Assert element is visible.
    
    Args:
        page: Playwright Page
        selector: Element selector
        timeout: Timeout in milliseconds
    """
    try:
        expect(page.locator(selector)).to_be_visible(timeout=timeout)
    except AssertionError:
        logger.error(f"Element not visible: {selector}")
        raise


def assert_element_hidden(page: Page, selector: str, timeout: int = 5000) -> None:
    """
    Assert element is hidden.
    
    Args:
        page: Playwright Page
        selector: Element selector
        timeout: Timeout in milliseconds
    """
    try:
        expect(page.locator(selector)).to_be_hidden(timeout=timeout)
    except AssertionError:
        logger.error(f"Element still visible: {selector}")
        raise


def assert_text_equals(page: Page, selector: str, expected_text: str) -> None:
    """
    Assert element text equals expected.
    
    Args:
        page: Playwright Page
        selector: Element selector
        expected_text: Expected text
    """
    expect(page.locator(selector)).to_have_text(expected_text)


def assert_text_contains(page: Page, selector: str, expected_text: str) -> None:
    """
    Assert element text contains expected.
    
    Args:
        page: Playwright Page
        selector: Element selector
        expected_text: Expected text substring
    """
    expect(page.locator(selector)).to_contain_text(expected_text)


def assert_url_contains(page: Page, expected_path: str) -> None:
    """
    Assert current URL contains expected path.
    
    Args:
        page: Playwright Page
        expected_path: Expected URL path or pattern
    """
    actual_url = page.url
    
    if expected_path not in actual_url:
        error_msg = f"Expected URL to contain '{expected_path}', got '{actual_url}'"
        logger.error(error_msg)
        raise AssertionError(error_msg)


# ============================================================================
# DATA ASSERTIONS
# ============================================================================

def assert_dict_contains(data: Dict, expected_keys: list, message: str = None) -> None:
    """
    Assert dictionary contains all expected keys.
    
    Args:
        data: Dictionary to check
        expected_keys: List of expected keys
        message: Optional custom error message
    """
    missing_keys = [key for key in expected_keys if key not in data]
    
    if missing_keys:
        error_msg = message or f"Missing keys: {missing_keys}"
        logger.error(error_msg)
        raise AssertionError(error_msg)

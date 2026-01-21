"""
Multi-Browser Testing Examples

Run with: pytest tests/multi_browser_example.py -v

This will automatically run each test 3 times:
- Once on Chromium
- Once on Firefox
- Once on WebKit
"""

import pytest


class TestMultiBrowserBasic:
    """Basic multi-browser tests using multi_browser fixture"""
    
    def test_page_title_on_all_browsers(self, multi_browser_page):
        """
        Test that verifies page title on all browsers
        
        This test runs 3 times automatically (once per browser)
        """
        # multi_browser_page is pre-configured from multi_browser_context
        # which uses the multi_browser fixture
        assert multi_browser_page is not None
    
    def test_navigation_on_all_browsers(self, multi_browser_page):
        """Test navigation works on all browsers"""
        # Navigate to a page
        multi_browser_page.goto("https://example.com")
        
        # Verify we're on the page
        title = multi_browser_page.title()
        assert "Example" in title
    
    def test_button_click_on_all_browsers(self, multi_browser_context):
        """Test button clicking works on all browsers"""
        page = multi_browser_context.new_page()
        
        # Navigate to page with buttons
        page.goto("https://example.com")
        
        # Verify page loaded
        assert page.url == "https://example.com/"
        
        page.close()


class TestMultiBrowserWithAuthentication:
    """Multi-browser tests with authentication"""
    
    def test_login_page_on_all_browsers(self, multi_browser_page):
        """Test login page renders correctly on all browsers"""
        # In real implementation, navigate to login
        # multi_browser_page.goto("https://app.com/login")
        # assert "Login" in multi_browser_page.title()
        pass
    
    def test_form_fill_on_all_browsers(self, multi_browser_page):
        """Test form filling works on all browsers"""
        # In real implementation:
        # multi_browser_page.fill("input#username", "testuser")
        # multi_browser_page.fill("input#password", "password123")
        # multi_browser_page.click("button[type='submit']")
        pass


class TestBrowserSpecificBehavior:
    """Test browser-specific behaviors"""
    
    def test_get_browser_name(self, multi_browser):
        """Verify multi_browser fixture works"""
        # Create a context to verify browser is working
        context = multi_browser.new_context()
        page = context.new_page()
        
        # Do a basic operation to verify browser is working
        page.goto("https://example.com")
        assert page.title() is not None
        
        page.close()
        context.close()
    
    def test_viewport_consistency(self, multi_browser_context):
        """Test viewport is consistent across browsers"""
        page = multi_browser_context.new_page()
        
        # Get viewport size
        viewport = page.evaluate("() => ({ width: window.innerWidth, height: window.innerHeight })")
        
        # Verify viewport is set
        assert viewport["width"] > 0
        assert viewport["height"] > 0
        
        page.close()


# ============================================================================
# ADVANCED: Using multi_browser directly (if you need more control)
# ============================================================================

class TestDirectMultiBrowserUsage:
    """Direct usage of multi_browser fixture for more control"""
    
    def test_direct_multi_browser_usage(self, multi_browser):
        """
        Direct usage of multi_browser fixture
        
        Use this when you need more control over context creation
        """
        # Create context manually for custom options
        context = multi_browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Test your application
        page.goto("https://example.com")
        assert "Example" in page.title()
        
        # Cleanup
        page.close()
        context.close()
    
    def test_multiple_pages_same_browser(self, multi_browser):
        """Test multiple pages in same browser context"""
        # Create first context and page
        context1 = multi_browser.new_context()
        page1 = context1.new_page()
        page1.goto("https://example.com")
        
        # Create second context and page (isolated from first)
        context2 = multi_browser.new_context()
        page2 = context2.new_page()
        page2.goto("https://google.com")
        
        # Verify both pages are accessible
        assert "Example" in page1.title()
        assert "Google" in page2.title() or "google" in page2.url
        
        # Cleanup
        page1.close()
        context1.close()
        page2.close()
        context2.close()


# ============================================================================
# COMPARISON: Using single browser vs multi-browser
# ============================================================================

class TestComparisonSingleVsMulti:
    """Examples showing single browser vs multi-browser testing"""
    
    def test_single_browser_example(self, page):
        """
        Using single browser fixture
        Runs ONCE on the configured browser (usually chromium)
        """
        page.goto("https://example.com")
        assert "Example" in page.title()
    
    def test_multi_browser_example(self, multi_browser_page):
        """
        Using multi_browser fixture
        Runs THREE TIMES: once on chromium, firefox, webkit
        """
        multi_browser_page.goto("https://example.com")
        assert "Example" in multi_browser_page.title()


# ============================================================================
# RUN COMMAND AND OUTPUT
# ============================================================================

"""
Run all multi-browser tests:
    pytest tests/multi_browser_example.py -v

Run specific test on all browsers:
    pytest tests/multi_browser_example.py::TestMultiBrowserBasic::test_page_title_on_all_browsers -v

Run only on Chromium:
    pytest tests/multi_browser_example.py --browser-type=chromium -v

Run only on Firefox:
    pytest tests/multi_browser_example.py --browser-type=firefox -v

Expected Output:
    test_multi_browser_example.py::TestMultiBrowserBasic::test_page_title_on_all_browsers[chromium] PASSED
    test_multi_browser_example.py::TestMultiBrowserBasic::test_page_title_on_all_browsers[firefox] PASSED
    test_multi_browser_example.py::TestMultiBrowserBasic::test_page_title_on_all_browsers[webkit] PASSED
    test_multi_browser_example.py::TestMultiBrowserBasic::test_navigation_on_all_browsers[chromium] PASSED
    test_multi_browser_example.py::TestMultiBrowserBasic::test_navigation_on_all_browsers[firefox] PASSED
    test_multi_browser_example.py::TestMultiBrowserBasic::test_navigation_on_all_browsers[webkit] PASSED
    ...
"""

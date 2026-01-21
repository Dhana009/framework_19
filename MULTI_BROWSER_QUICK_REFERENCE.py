"""
MULTI-BROWSER TESTING - QUICK REFERENCE
========================================

Updated Framework: browser_fixtures.py now includes multi_browser fixture
"""

# ============================================================================
# QUICK START - COPY-PASTE READY
# ============================================================================

# OPTION 1: Use multi_browser_page (EASIEST)
# ==========================================

def test_cross_browser_simple(multi_browser_page):
    """
    Simplest way - just use multi_browser_page
    Runs 3 times automatically
    """
    multi_browser_page.goto("https://example.com")
    assert "Example" in multi_browser_page.title()
    # DONE! Runs on: chromium, firefox, webkit


# OPTION 2: Use multi_browser_context (MORE CONTROL)
# ===================================================

def test_cross_browser_with_context(multi_browser_context):
    """
    Use when you need custom page options
    Runs 3 times automatically
    """
    page = multi_browser_context.new_page()
    page.goto("https://example.com")
    assert "Example" in page.title()
    page.close()
    # DONE! Runs on: chromium, firefox, webkit


# OPTION 3: Use multi_browser (MOST CONTROL)
# ============================================

def test_cross_browser_advanced(multi_browser):
    """
    Use when you need full control
    Runs 3 times automatically
    """
    context = multi_browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()
    page.goto("https://example.com")
    assert "Example" in page.title()
    page.close()
    context.close()
    # DONE! Runs on: chromium, firefox, webkit


# ============================================================================
# COMMAND-LINE USAGE
# ============================================================================

"""
Run all tests on all browsers:
    pytest tests/sanity/ -v
    
    Output:
    test_login.py::test_login[chromium] PASSED
    test_login.py::test_login[firefox] PASSED
    test_login.py::test_login[webkit] PASSED

Run specific test file:
    pytest tests/sanity/test_login.py -v

Run specific test class:
    pytest tests/sanity/test_login.py::TestLogin -v

Run specific test:
    pytest tests/sanity/test_login.py::TestLogin::test_user_login -v

Run only on Chromium:
    pytest --browser-type=chromium tests/ -v

Run only on Firefox:
    pytest --browser-type=firefox tests/ -v

Run only on WebKit:
    pytest --browser-type=webkit tests/ -v

Run in headless mode:
    pytest --headless tests/ -v

Run with HTML report:
    pytest tests/ --html=reports/report.html -v

Run with Allure report:
    pytest tests/ --alluredir=reports/allure-results -v
"""


# ============================================================================
# FIXTURE HIERARCHY (UPDATED)
# ============================================================================

"""
For Single Browser Testing:
===========================
config
  ↓
playwright_instance
  ↓
browser_manager
  ↓
browser ← Use this for single browser tests
  ↓
context_manager
  ↓
context ← Fresh isolated context
  ↓
page ← Ready to use

For Multi-Browser Testing:
===========================
config
  ↓
playwright_instance
  ↓
browser_manager
  ↓
multi_browser ← Use this for cross-browser tests (parametrized)
  ├─ [chromium] ← Test runs on chromium
  ├─ [firefox] ← Test runs on firefox
  └─ [webkit] ← Test runs on webkit
    ↓
multi_browser_context ← Fresh context per browser
    ↓
multi_browser_page ← Fresh page per browser
"""


# ============================================================================
# REAL-WORLD EXAMPLES
# ============================================================================

# Example 1: Cross-Browser Login Test
# ====================================
def test_login_all_browsers(multi_browser_page):
    """
    Login test that runs on all 3 browsers
    """
    multi_browser_page.goto("https://app.com/login")
    
    # Verify login page loads on all browsers
    assert "Login" in multi_browser_page.title()
    
    # Fill form
    multi_browser_page.fill("input#username", "testuser")
    multi_browser_page.fill("input#password", "password123")
    multi_browser_page.click("button[type='submit']")
    
    # Wait and verify
    multi_browser_page.wait_for_load_state("networkidle")
    assert "Dashboard" in multi_browser_page.title()


# Example 2: Cross-Browser Responsive Test
# ==========================================
def test_responsive_design(multi_browser):
    """
    Test responsive design on all browsers
    """
    # Different viewports for different browsers
    viewports = [
        {"name": "mobile", "width": 375, "height": 667},
        {"name": "tablet", "width": 768, "height": 1024},
        {"name": "desktop", "width": 1920, "height": 1080},
    ]
    
    for viewport in viewports:
        context = multi_browser.new_context(viewport={
            "width": viewport["width"],
            "height": viewport["height"]
        })
        page = context.new_page()
        
        page.goto("https://app.com")
        
        # Verify layout is correct for this viewport
        body_width = page.evaluate("() => document.body.clientWidth")
        assert body_width == viewport["width"]
        
        page.close()
        context.close()


# Example 3: Cross-Browser Form Submission
# ==========================================
def test_form_submission_all_browsers(multi_browser_page):
    """
    Form submission test on all 3 browsers
    """
    multi_browser_page.goto("https://app.com/form")
    
    # Fill form
    multi_browser_page.fill("input#name", "John Doe")
    multi_browser_page.fill("input#email", "john@example.com")
    multi_browser_page.fill("textarea#message", "Test message")
    
    # Submit
    multi_browser_page.click("button[type='submit']")
    
    # Verify success
    multi_browser_page.wait_for_load_state("networkidle")
    assert "Success" in multi_browser_page.content()


# ============================================================================
# INTERVIEW ANSWER - MULTI-BROWSER TESTING
# ============================================================================

"""
Q: "How do you test on multiple browsers?"

A: "I updated the framework to support parametrized multi-browser testing.

Here's what I did:

1. Added 'multi_browser' fixture in browser_fixtures.py
   - Parametrized with @pytest.fixture(params=["chromium", "firefox", "webkit"])
   - Automatically launches each browser type

2. Created helper fixtures:
   - multi_browser_context: fresh context for each browser
   - multi_browser_page: ready-to-use page for each browser

3. Usage is simple:
   ```python
   def test_something(multi_browser_page):
       multi_browser_page.goto('https://example.com')
       assert 'Example' in multi_browser_page.title()
   ```

4. When I run pytest, this test automatically runs 3 times:
   - Once on Chromium
   - Once on Firefox
   - Once on WebKit

5. Each browser runs in isolation, so no interference between tests

Benefits:
- No code duplication
- Single test file covers all browsers
- Easy to run: just pytest tests/
- Can still run single browser: pytest --browser-type=chromium

Example test runs:
  test_login.py::test_something[chromium] PASSED
  test_login.py::test_something[firefox] PASSED
  test_login.py::test_something[webkit] PASSED"
"""


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Q: Test runs multiple times, I only want it once
A: Use the regular 'page' fixture instead of 'multi_browser_page'
   def test_something(page):
       page.goto('https://example.com')

Q: How do I know which browser is running?
A: Add print in your test:
   def test_something(multi_browser_page):
       # Can't directly know, but you can check user agent
       ua = multi_browser_page.evaluate("() => navigator.userAgent")
       print(f"User Agent: {ua}")

Q: I want to skip a test on specific browsers
A: Use markers:
   @pytest.mark.skip(reason="Bug in webkit")
   def test_something(multi_browser_page):
       pass

Q: How do I run only on Chromium?
A: Use CLI option:
   pytest --browser-type=chromium tests/

Q: Performance is slow with 3 browsers
A: Use --browser-type to run one browser at a time:
   pytest --browser-type=chromium tests/ &
   pytest --browser-type=firefox tests/ &
   pytest --browser-type=webkit tests/ &
"""


# ============================================================================
# CHEAT SHEET
# ============================================================================

"""
BEFORE (Single Browser):
    pytest tests/
    → Runs all tests on Chromium only

AFTER (Multi-Browser):
    pytest tests/
    → Runs all tests on Chromium, Firefox, WebKit automatically
    → Test runs 3X but only write once!

Just change:
    def test_something(page):
To:
    def test_something(multi_browser_page):

That's it! Auto-runs on all 3 browsers.
"""

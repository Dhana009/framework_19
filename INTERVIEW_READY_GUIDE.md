# INTERVIEW READY FRAMEWORK GUIDE
## Quick Reference for Practical Interview Questions

---

## 1. FRAMEWORK ARCHITECTURE OVERVIEW

### What We Have:
```
├── API Testing Layer
│   ├── APIClient (HTTP transport + retry logic)
│   ├── AuthAPI (authentication operations)
│   └── UserAPI (user operations)
├── UI Testing Layer
│   ├── BrowserManager (launch browser)
│   ├── ContextManager (create isolated contexts)
│   └── AuthManager (handle authentication)
├── Fixtures (Setup/teardown)
│   ├── browser_fixtures.py → Launch ONE browser for session
│   ├── auth_fixtures.py → Handle authentication once
│   ├── context_fixtures.py → Fresh context + page per test
│   ├── api_fixtures.py → Authenticated API clients
│   └── data_fixtures.py → Test data
└── Configuration
    ├── env_config.yaml
    ├── test_config.yaml
    └── config_loader.py
```

---

## 2. QUICK COMPONENT SUMMARY

### APIClient (api/api_client.py)
```
Purpose: HTTP client with retry logic
Responsibilities:
- Manage HTTP sessions
- Send GET, POST, PUT, PATCH, DELETE
- Handle retries with exponential backoff
- Set headers, auth tokens
- Log requests/responses
```

### AuthAPI (api/auth_api.py)
```
Purpose: Authentication operations
Responsibilities:
- login(username, password) → get token
- refresh_token(token) → get new token
- logout(token) → invalidate token
- validate_token(token) → check validity
```

### UserAPI (api/user_api.py)
```
Purpose: User operations
Responsibilities:
- create_user(payload) → create user
- get_user(user_id) → fetch user
- update_user(user_id, payload) → update user
- delete_user(user_id) → delete user
```

### BrowserManager (core/browser_manager.py)
```
Purpose: Browser launch logic
Responsibilities:
- Launch browser (chromium/firefox/webkit)
- Configure: headless, viewport, slowmo, args
- Get context options (viewport, timezone, locale)
Does NOT: manage lifecycle, create contexts
```

### ContextManager (core/context_manager.py)
```
Purpose: Create isolated contexts
Responsibilities:
- Create context with options
- Load storage_state (auth persistence)
- Create pages from contexts
Does NOT: manage lifecycle, validate auth
```

### AuthManager (core/auth_manager.py)
```
Purpose: Authentication mechanics
Responsibilities:
- authenticate_via_ui() → login + save storage_state
- authenticate_via_api() → login + return tokens
- is_storage_state_valid() → check expiration
- validate_auth_state(page, url) → test auth
- clear_storage_state() → delete saved auth
Does NOT: control when to authenticate
```

---

## 3. FIXTURES QUICK REFERENCE

### browser_fixtures.py
```
config → Load configuration (session)
playwright_instance → Initialize Playwright (session)
browser_manager → Create BrowserManager (session)
browser → Launch browser (session)
         Output: ONE browser for all tests
```

### auth_fixtures.py
```
auth_manager → Create AuthManager (session)
auth_state → Check/create authentication (session)
           - If valid: return path (FAST!)
           - If invalid: authenticate and save
fresh_auth → Force fresh login (function)
```

### context_fixtures.py
```
context_manager → Create ContextManager (function)
context → Fresh context with auth (function)
        - Gets storage_state from auth_state
        - Creates isolated context
        Output: Fresh isolated session per test
page → Create page from context (function)
     Output: Ready-to-use page per test
unauthenticated_context → Context WITHOUT auth (function)
unauthenticated_page → Page WITHOUT auth (function)
```

### api_fixtures.py
```
api_client → Base HTTP client (session)
authenticated_api_client → HTTPclient + token (session)
auth_api → AuthAPI instance (session)
user_api → UserAPI instance (session)
```

---

## 4. QUICK CODE SNIPPETS FOR INTERVIEW

### How to Write a Simple API Test
```python
def test_create_user(user_api):
    """Test creating a user via API"""
    response = user_api.create_user({
        "username": "john_doe",
        "email": "john@example.com"
    })
    assert response["id"] > 0
    assert response["username"] == "john_doe"
```

### How to Write a UI Test
```python
def test_login_and_view_dashboard(page):
    """Test login flow"""
    page.goto("https://app.com/login")
    page.fill("input#username", "john_doe")
    page.fill("input#password", "password123")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    assert "Dashboard" in page.title()
```

### How to Write an Unauthenticated Test
```python
def test_login_required(unauthenticated_page):
    """Test that dashboard requires login"""
    unauthenticated_page.goto("https://app.com/dashboard")
    # Should redirect to login
    assert "/login" in unauthenticated_page.url
```

### How to Create APIClient
```python
from api.api_client import APIClient

client = APIClient(
    base_url="https://api.example.com",
    timeout=30,
    retry_config={
        "max_attempts": 3,
        "backoff_factor": 2,
        "retry_on_status_codes": [500, 502, 503, 504]
    }
)

# Use it
response = client.get("/users")
response = client.post("/users", json={"name": "John"})
```

### How to Create BrowserManager
```python
from core.browser_manager import BrowserManager

config = {
    "type": "chromium",
    "headless": True,
    "viewport": {"width": 1920, "height": 1080},
    "slowmo": 500,
    "args": []
}

manager = BrowserManager(config)
browser = manager.launch(playwright)  # playwright from sync_playwright()
```

### How to Create ContextManager
```python
from core.context_manager import ContextManager

manager = ContextManager(
    browser=browser,
    default_options={
        "viewport": {"width": 1920, "height": 1080},
        "timezone_id": "America/New_York"
    }
)

# Create isolated contexts
context1 = manager.create_context(storage_state="auth1.json")
context2 = manager.create_context(storage_state="auth2.json")

page1 = manager.create_page_from_context(context1)
page2 = manager.create_page_from_context(context2)
```

### How to Create AuthManager
```python
from core.auth_manager import AuthManager

config = {
    "storage_state_path": "auth_state/storage_state.json",
    "token_validity_seconds": 3600
}

manager = AuthManager(config)

# Check if auth is valid
if manager.is_storage_state_valid():
    path = manager.get_storage_state_path()
    # Use existing auth
else:
    # Need to authenticate
    manager.authenticate_via_ui(page, "https://app.com/login", {
        "username": "john",
        "password": "pass"
    })
```

---

## 5. CONFIGURATION EXAMPLES

### How to Read Configuration
```python
from config.config_loader import get_config

# In pytest fixture
config = get_config(request)

# Access properties
api_base_url = config.api_base_url
browser_config = config.browser_config
auth_config = config.auth_config
timeout = config.timeouts.get("api_request", 30000)
```

### Configuration Files Location
```
config/
├── env_config.yaml (environment-specific: qa, staging, prod)
├── test_config.yaml (general test settings)
└── config_loader.py (loads and parses configs)
```

### What's in test_config.yaml
```yaml
browser:
  type: chromium
  headless: false
  viewport:
    width: 1920
    height: 1080
  slowmo: 0

api:
  base_url: https://api.qa.example.com
  timeout: 30000
  retry_config:
    max_attempts: 3
    backoff_factor: 2

auth:
  storage_state_path: auth_state/storage_state.json
  token_validity_seconds: 3600
  
credentials:
  username: test_user
  password: test_password
```

---

## 6. RUNNING TESTS - COMMAND EXAMPLES

### Run All Tests
```bash
pytest
```

### Run with Specific Environment
```bash
pytest --env=qa
pytest --env=staging
```

### Run with Specific Browser
```bash
pytest --browser-type=chromium
pytest --browser-type=firefox
```

### Run Headless (No GUI)
```bash
pytest --headless
```

### Run Specific Test
```bash
pytest tests/sanity/test_login_smoke.py::test_login
```

### Run Tests with Marker
```bash
pytest -m api  # Run API tests
pytest -m ui   # Run UI tests
```

### Run with Allure Report
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 7. TROUBLESHOOTING QUICK ANSWERS

### Q: "How do I write a test that doesn't use auth?"
**A:** Use `unauthenticated_page` fixture instead of `page`
```python
def test_login_page(unauthenticated_page):
    unauthenticated_page.goto("/login")
```

### Q: "How do I retry a test?"
**A:** Use pytest retry marker
```python
@pytest.mark.flaky(reruns=3)
def test_something(page):
    page.goto("/dashboard")
```

### Q: "How do I add custom headers?"
**A:** Use `set_header()` on APIClient
```python
client.set_header("X-Custom-Header", "value")
```

### Q: "How do I set auth token?"
**A:** Use `set_auth_token()` on APIClient
```python
client.set_auth_token(token, token_type="Bearer")
```

### Q: "How do I get auth tokens via API?"
**A:** Use AuthAPI
```python
auth_data = auth_api.login("username", "password")
token = auth_data["access_token"]
```

### Q: "How do I validate a page is authenticated?"
**A:** Use AuthManager
```python
is_valid = auth_manager.validate_auth_state(page, "/dashboard")
```

---

## 8. DEPENDENCY CHAIN (Interview Question)

```
Test Execution Chain:

conftest.py
  ├─ Registers all fixture modules
  ├─ Defines CLI options (--env, --browser-type, --headless)
  └─ Defines global hooks
       ↓
browser_fixtures.py
  ├─ config → loads from YAML
  ├─ playwright_instance → Playwright(...)
  ├─ browser_manager → BrowserManager(config)
  └─ browser → browser_manager.launch()
       ↓
auth_fixtures.py
  ├─ auth_manager → AuthManager(config)
  └─ auth_state → authenticate if needed, return path
       ↓
context_fixtures.py
  ├─ context_manager → ContextManager(browser)
  ├─ context → create context with auth_state
  └─ page → create page from context
       ↓
Test receives: page (already authenticated, ready to use)
```

---

## 9. INTERVIEW SCENARIOS - QUICK ANSWERS

### Scenario 1: "Write an API test that creates a user"
```python
def test_create_user_api(user_api):
    response = user_api.create_user({
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    assert response["id"] > 0
```

### Scenario 2: "Write a UI test that logs in and checks dashboard"
```python
def test_user_dashboard(page):
    page.goto("https://app.com/dashboard")
    assert "Welcome" in page.title()
```

### Scenario 3: "Write a test that needs fresh login"
```python
def test_login_flow(fresh_auth, unauthenticated_page):
    unauthenticated_page.goto("https://app.com/login")
    unauthenticated_page.fill("input#username", "john")
    unauthenticated_page.fill("input#password", "pass123")
    unauthenticated_page.click("button[type='submit']")
    unauthenticated_page.wait_for_load_state("networkidle")
    assert "Dashboard" in unauthenticated_page.title()
```

### Scenario 4: "Create an API client from scratch"
```python
from api.api_client import APIClient

def test_api_client():
    client = APIClient(
        base_url="https://api.example.com",
        timeout=30,
        retry_config={
            "max_attempts": 3,
            "backoff_factor": 2
        }
    )
    
    # Make request
    response = client.get("/users")
    assert response.status_code == 200
    
    client.close()
```

---

## 10. KEY INTERVIEW POINTS TO REMEMBER

1. **APIClient** = Transport layer (how to send HTTP)
2. **AuthAPI/UserAPI** = Business logic (what to do with HTTP)
3. **BrowserManager** = Launch browser
4. **ContextManager** = Create isolated sessions
5. **AuthManager** = Handle authentication state
6. **Fixtures** = Orchestrate when things happen
7. **Session scope** = Reused across all tests (fast!)
8. **Function scope** = Fresh for each test (isolation!)
9. **storage_state.json** = Persistent authentication (no re-login)
10. **Dependency Injection** = Tests receive pre-built fixtures

---

## 11. FRAMEWORK READINESS CHECKLIST

✅ **API Layer**
- APIClient ready (GET, POST, PUT, PATCH, DELETE)
- AuthAPI ready (login, refresh, logout, validate)
- UserAPI ready (CRUD operations)

✅ **UI Layer**
- BrowserManager ready (launches browser)
- ContextManager ready (creates contexts/pages)
- AuthManager ready (UI/API auth, validation)

✅ **Fixtures**
- browser_fixtures.py ready
- auth_fixtures.py ready
- context_fixtures.py ready
- api_fixtures.py ready
- data_fixtures.py ready

✅ **Configuration**
- test_config.yaml configured
- env_config.yaml configured
- config_loader.py working

✅ **conftest.py**
- All fixture modules registered
- CLI options defined
- Global hooks configured

✅ **Ready for Interview**
- All components documented
- Quick reference available
- Code snippets ready
- Common scenarios prepared

---

## 12. MULTIPLE BROWSER TESTING (FRAMEWORK UPDATED)

### Framework Update - What Was Added

**Files Updated:**
- ✅ `fixtures/browser_fixtures.py` - Added `multi_browser` fixture
- ✅ `fixtures/context_fixtures.py` - Added `multi_browser_context` and `multi_browser_page` fixtures
- ✅ New file: `tests/multi_browser_example.py` - Practical examples
- ✅ New file: `MULTI_BROWSER_QUICK_REFERENCE.py` - Quick reference

---

### The Easiest Way - Use multi_browser_page

```python
def test_login_all_browsers(multi_browser_page):
    """
    This test runs 3 times automatically:
    - Once on Chromium
    - Once on Firefox  
    - Once on WebKit
    """
    multi_browser_page.goto("https://app.com/login")
    multi_browser_page.fill("input#username", "john")
    multi_browser_page.fill("input#password", "pass123")
    multi_browser_page.click("button[type='submit']")
    assert "Dashboard" in multi_browser_page.title()
```

**That's it!** Just change `page` to `multi_browser_page` and it runs on all 3 browsers automatically.

---

### Three Fixture Options

#### Option 1: multi_browser_page (EASIEST)
```python
def test_something(multi_browser_page):
    multi_browser_page.goto("https://example.com")
    assert "Example" in multi_browser_page.title()
```
- Best for quick tests
- Pre-configured page ready to use
- Just like the regular `page` fixture but runs 3X

#### Option 2: multi_browser_context (MORE CONTROL)
```python
def test_something(multi_browser_context):
    page = multi_browser_context.new_page()
    page.goto("https://example.com")
    assert "Example" in page.title()
    page.close()
```
- When you need to create multiple pages in one test
- Full access to context options

#### Option 3: multi_browser (MOST CONTROL)
```python
def test_something(multi_browser):
    context = multi_browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
    page.goto("https://example.com")
    assert "Example" in page.title()
    page.close()
    context.close()
```
- When you need custom viewport, options
- Most flexibility

---

### Running Tests

#### Run All Tests on All Browsers
```bash
pytest tests/ -v
```
**Output:**
```
test_login.py::test_login[chromium] PASSED
test_login.py::test_login[firefox] PASSED
test_login.py::test_login[webkit] PASSED
```

#### Run Only on Specific Browser
```bash
pytest --browser-type=chromium tests/ -v
pytest --browser-type=firefox tests/ -v
pytest --browser-type=webkit tests/ -v
```

#### Run Specific Test File
```bash
pytest tests/sanity/test_login.py -v
```

#### Run in Headless Mode
```bash
pytest --headless tests/ -v
```

---

### How It Works - Behind the Scenes

```
When you write:
    def test_login(multi_browser_page):

Pytest sees:
    @pytest.fixture(params=["chromium", "firefox", "webkit"])
    def multi_browser(request):
        ...

And automatically runs your test 3 times:
    test_login[chromium] → launches Firefox, runs test
    test_login[firefox] → launches Firefox, runs test
    test_login[webkit] → launches WebKit, runs test
```

---

### Real Examples from tests/multi_browser_example.py

```python
# Example 1: Simple cross-browser test
def test_page_title_on_all_browsers(multi_browser_page):
    assert multi_browser_page is not None

# Example 2: Navigation test
def test_navigation_on_all_browsers(multi_browser_page):
    multi_browser_page.goto("https://example.com")
    title = multi_browser_page.title()
    assert "Example" in title

# Example 3: Form test
def test_form_fill_on_all_browsers(multi_browser_page):
    multi_browser_page.goto("https://app.com/form")
    multi_browser_page.fill("input#username", "testuser")
    multi_browser_page.click("button[type='submit']")

# Example 4: Multiple pages in same browser
def test_multiple_pages_same_browser(multi_browser):
    context1 = multi_browser.new_context()
    page1 = context1.new_page()
    page1.goto("https://example.com")
    
    context2 = multi_browser.new_context()
    page2 = context2.new_page()
    page2.goto("https://google.com")
    
    page1.close()
    context1.close()
    page2.close()
    context2.close()
```

---

### Interview Answer for Multi-Browser Testing

> *"I updated the framework to support cross-browser testing.*
>
> *Here's what I added:*
>
> *1. `multi_browser` fixture in browser_fixtures.py with parametrization for chromium, firefox, webkit*
>
> *2. Helper fixtures:*
> *   - `multi_browser_page` - for quick tests*
> *   - `multi_browser_context` - for tests needing multiple pages*
>
> *3. Usage is simple: just use `multi_browser_page` instead of `page`*
>
> *4. When you run `pytest tests/ -v`, each test automatically runs 3 times - once per browser*
>
> *5. Benefits:*
> *   - Write test once, runs on all 3 browsers*
> *   - No code duplication*
> *   - Each browser is isolated, no interference*
> *   - Can still run single browser with `--browser-type=chromium`*
>
> *Example:*
> ```python
> def test_login(multi_browser_page):
>     multi_browser_page.goto('/login')
>     assert 'Login' in multi_browser_page.title()
> ```
>
> *This runs 3 times automatically.*
>
> *The implementation uses pytest's parametrize feature which runs the fixture with different values, triggering the test execution multiple times."*

---

### Quick Comparison: Before vs After

**BEFORE (Single Browser):**
```python
def test_login(page):
    page.goto("/login")
    assert "Login" in page.title()
```
- Runs 1 time (on Chromium)

**AFTER (Multi-Browser):**
```python
def test_login(multi_browser_page):
    multi_browser_page.goto("/login")
    assert "Login" in multi_browser_page.title()
```
- Runs 3 times (Chromium, Firefox, WebKit)
- Only changed `page` to `multi_browser_page`!

---

### Fixture Dependency Chain (UPDATED)

```
config
  ↓
playwright_instance
  ↓
browser_manager
  ├─→ browser (single browser)
  └─→ multi_browser (parametrized for all 3 browsers)
       ├─ [chromium]
       ├─ [firefox]
       └─ [webkit]
  ↓
For single browser:
context_manager → context → page

For multi-browser:
multi_browser_context → multi_browser_page
```

---

## 13. DURING INTERVIEW - DO THIS

1. **If asked to write code:**
   - Use snippets from Section 4 or Section 12
   - Explain each line
   - Ask "Does this look good?"

2. **If asked about multiple browsers:**
   - Show Approach 1 (Parametrization) - it's cleanest
   - Explain: "Same test, runs 3 times automatically"
   - Show the CLI command

3. **If asked about configuration:**
   - Reference Section 5
   - Show where files are
   - Explain what each field does

4. **If asked to debug:**
   - Check fixture dependencies (Section 9)
   - Check configuration (Section 5)
   - Use print statements to debug

5. **If running out of time:**
   - Just explain what you'd do
   - Don't write buggy code
   - Show understanding > perfect code

---

**GOOD LUCK WITH YOUR INTERVIEW! 🚀**

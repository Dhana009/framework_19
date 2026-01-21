# Quick Start Guide - Simplified Framework

Perfect for 1-hour interviews! Clean, minimal, and fully functional.

---

## Directory Structure

```
simple_framework/
├── conftest.py              ← Fixtures (browser, page, api_client)
├── config.yaml              ← Configuration (browser, urls, credentials)
├── pytest.ini               ← Pytest settings
├── README.md                ← Overview
├── api/
│   ├── __init__.py
│   └── api_client.py        ← HTTP client (GET, POST, PUT, DELETE)
└── tests/
    ├── api/
    │   ├── __init__.py
    │   └── test_api.py      ← API test examples
    └── ui/
        ├── __init__.py
        └── test_ui.py       ← UI test examples
```

---

## Installation

```bash
cd simple_framework

pip install pytest playwright pyyaml requests

playwright install chromium firefox webkit
```

---

## Run Tests

### All Tests
```bash
pytest tests/ -v
```

### API Tests Only
```bash
pytest tests/api/ -v
```

### UI Tests Only
```bash
pytest tests/ui/ -v
```

### Specific Test
```bash
pytest tests/api/test_api.py::TestGetRequests::test_get_users -v
```

---

## CLI Options

### Change Browser
```bash
pytest tests/ -v --browser chromium
pytest tests/ -v --browser firefox
pytest tests/ -v --browser webkit
```

### Headless Mode
```bash
pytest tests/ -v --headless
```

### With Browser Visible
```bash
pytest tests/ -v
```

### Slow Motion (easier to see actions)
Edit `config.yaml`:
```yaml
browser:
  slowmo: 1000  # 1 second delay between actions
```

---

## Interview Walkthrough (1 Hour)

### 5 Minutes: Show Structure
```bash
# Show the directory
ls -la simple_framework/

# Show config
cat config.yaml

# Show conftest.py (explain fixtures)
```

### 10 Minutes: Explain Each Component
1. **config.yaml** - "Configuration for browser, URLs, credentials"
2. **conftest.py** - "Fixtures that setup browser, page, API client"
3. **api/api_client.py** - "Simple HTTP client for API calls"
4. **tests/api/test_api.py** - "API test examples"
5. **tests/ui/test_ui.py** - "UI test examples"

### 15 Minutes: Run Tests
```bash
pytest tests/ -v
```
Show it running and passing

### 20 Minutes: Write a Simple Test
Create new file: `tests/api/test_custom.py`

```python
def test_example(api_client):
    response = api_client.get("/users")
    assert response is not None
```

Run it:
```bash
pytest tests/api/test_custom.py -v
```

### 10 Minutes: Show CLI Options
```bash
pytest tests/ --browser firefox -v
pytest tests/ --headless -v
pytest tests/api/ -v
```

---

## Key Components Explained

### conftest.py (Most Important)

```python
@pytest.fixture(scope="session")
def browser(config, playwright_instance, request):
    """
    Launches browser ONCE per session
    - scope="session" means ONE browser for all tests
    - Different browsers: chromium, firefox, webkit
    """
```

```python
@pytest.fixture(scope="function")
def page(context, config):
    """
    Creates fresh page FOR EACH TEST
    - scope="function" means new page per test
    - Ensures test isolation
    """
```

```python
@pytest.fixture(scope="session")
def api_client(config):
    """
    Creates API client ONCE per session
    - Reused across all API tests
    - Efficient
    """
```

### config.yaml

```yaml
browser:
  type: chromium  # Browser type
  headless: false # Show GUI
  slowmo: 500     # Delay between actions (ms)
  viewport:
    width: 1920
    height: 1080

api:
  base_url: https://api.example.com  # API server
  timeout: 30

ui:
  base_url: https://app.example.com  # App server
  wait_timeout: 10000
```

### api/api_client.py

```python
class APIClient:
    def get(self, endpoint):      # GET request
    def post(self, endpoint, json):  # POST request
    def put(self, endpoint, json):   # PUT request
    def delete(self, endpoint):      # DELETE request
```

---

## Interview Questions You Can Answer

**Q: "How does your framework work?"**
```
A: "We have fixtures that setup browser and API client. 
   conftest.py provides fixtures with different scopes:
   - Browser is session scope (reused)
   - Page is function scope (fresh per test)
   - Tests use these fixtures as parameters"
```

**Q: "How do you change browser?"**
```
A: "Use CLI option: pytest --browser firefox
   This gets passed to pytest_addoption, 
   which selects the right browser launcher"
```

**Q: "How do you configure URLs?"**
```
A: "All in config.yaml. Loaded in conftest.py config fixture.
   Tests receive config through fixtures"
```

**Q: "Explain the fixture hierarchy"**
```
A: "config fixture loads YAML
   browser fixture launches browser
   context fixture creates context in browser
   page fixture creates page in context
   Tests receive these as parameters"
```

**Q: "Why use fixtures?"**
```
A: "Fixtures handle setup/teardown automatically.
   Tests just receive what they need.
   Easy to reuse, maintain, and extend"
```

---

## Expected Test Output

```
$ pytest tests/ -v

simple_framework/tests/api/test_api.py::TestGetRequests::test_get_users PASSED
simple_framework/tests/api/test_api.py::TestGetRequests::test_get_user_by_id PASSED
simple_framework/tests/api/test_api.py::TestPostRequests::test_create_user PASSED
simple_framework/tests/api/test_api.py::TestPutRequests::test_update_user PASSED
simple_framework/tests/api/test_api.py::TestDeleteRequests::test_delete_user PASSED
simple_framework/tests/ui/test_ui.py::TestNavigation::test_page_loads PASSED
simple_framework/tests/ui/test_ui.py::TestLogin::test_login_page_visible PASSED
simple_framework/tests/ui/test_ui.py::TestLogin::test_login_form_elements PASSED
simple_framework/tests/ui/test_ui.py::TestFormInteraction::test_fill_form PASSED
simple_framework/tests/ui/test_ui.py::TestPageTitle::test_homepage_title PASSED

================ 10 passed in 0.45s ================
```

---

## What Makes This Perfect for Interviews

✅ **Simple** - Anyone can understand in minutes  
✅ **Functional** - Actually works (not just theory)  
✅ **CLI-Driven** - Show commands in terminal  
✅ **Well-Organized** - Clear structure  
✅ **Documented** - Each file has comments  
✅ **Extensible** - Easy to add more tests  
✅ **Interview-Sized** - Can explain in 1 hour  
✅ **Real Patterns** - Session/function scope fixtures  
✅ **Shows Understanding** - Demonstrates framework design  

---

## Common Interview Modifications

### "Add an API test that checks response"
```python
def test_get_users_status(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200  # Add this
```

### "Add a UI test with form filling"
```python
def test_login_success(page, config):
    page.goto(f"{config['ui']['base_url']}/login")
    page.fill("input#username", "testuser")
    page.fill("input#password", "testpass")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    assert "Dashboard" in page.title()
```

### "Add authentication to API"
```python
def test_api_with_auth(api_client):
    api_client.set_auth_token("your_token_here")
    response = api_client.get("/users")
    assert response.status_code == 200
```

### "Run tests on multiple browsers"
```bash
pytest tests/ui/test_ui.py --browser chromium -v
pytest tests/ui/test_ui.py --browser firefox -v
pytest tests/ui/test_ui.py --browser webkit -v
```

---

**Ready for your interview!** 🚀

Just go into `simple_framework` directory and run `pytest tests/ -v`

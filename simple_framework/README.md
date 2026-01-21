# Simplified Test Framework - Interview Ready

A minimal, clean test framework for API and UI testing. Built for 1-hour interview scenarios.

## Structure

```
simple_framework/
├── conftest.py              # Fixtures & setup
├── config.yaml              # Configuration
├── api/
│   └── api_client.py        # HTTP client
├── tests/
│   ├── api/
│   │   └── test_api.py
│   └── ui/
│       └── test_ui.py
└── README.md
```

## Quick Start

### Run All Tests
```bash
pytest simple_framework/tests/ -v
```

### Run API Tests Only
```bash
pytest simple_framework/tests/api/ -v
```

### Run UI Tests Only
```bash
pytest simple_framework/tests/ui/ -v
```

### Run Headless (No GUI)
```bash
pytest simple_framework/tests/ -v --headless
```

### Run on Firefox
```bash
pytest simple_framework/tests/ -v --browser firefox
```

### Run on Chromium
```bash
pytest simple_framework/tests/ -v --browser chromium
```

## Components

### 1. API Client (api/api_client.py)
- Send HTTP requests (GET, POST, PUT, DELETE)
- Automatic retries
- JSON handling

### 2. Fixtures (conftest.py)
- Browser fixture (session scope)
- Page fixture (function scope)
- API client fixture
- Configuration loader

### 3. Configuration (config.yaml)
- Base URLs
- Browser settings
- Timeouts
- Credentials

### 4. Tests
- API tests: tests/api/test_api.py
- UI tests: tests/ui/test_ui.py

## Example Tests

### API Test
```python
def test_get_users(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
```

### UI Test
```python
def test_login(page):
    page.goto("https://app.com/login")
    page.fill("input#username", "user")
    page.fill("input#password", "pass")
    page.click("button[type='submit']")
    assert "Dashboard" in page.title()
```

## Interview-Friendly Features

✅ Simple and clean  
✅ Well-documented  
✅ CLI options for browser and mode  
✅ API + UI testing  
✅ Configuration management  
✅ Fixture-based setup  
✅ Can explain everything in 1 hour  
✅ Easy to extend  

## How to Present in Interview

1. **Show the structure** - "This is our framework structure"
2. **Explain conftest.py** - "These are our fixtures"
3. **Show config.yaml** - "Here's how we configure everything"
4. **Show API client** - "This handles all HTTP communication"
5. **Show a test** - "Here's how you write a test"
6. **Run a test** - "Let me show you it running"

Perfect for 1-hour interview!

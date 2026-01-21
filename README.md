# Test Automation Framework

## 🎯 Overview

Production-ready **Pytest + Playwright** automation framework demonstrating enterprise-level test automation architecture with clear separation of concerns, reusable authentication, and comprehensive testing capabilities.

## 🏗️ Architecture

```
automation-framework/
│
├── pytest.ini                     # Pytest configuration & markers
├── conftest.py                    # Orchestration layer
│
├── config/                        # Configuration management
│   ├── env_config.yaml           # Environment-specific settings
│   ├── test_config.yaml          # Execution settings
│   └── config_loader.py          # Configuration resolver
│
├── core/                          # Core infrastructure
│   ├── browser_manager.py        # Browser launch logic
│   ├── context_manager.py        # Context creation
│   └── auth_manager.py           # Authentication mechanics
│
├── api/                           # API layer
│   ├── api_client.py             # HTTP client with retries
│   ├── auth_api.py               # Auth endpoints
│   └── user_api.py               # User endpoints
│
├── fixtures/                      # Pytest fixtures (lifecycle orchestration)
│   ├── browser_fixtures.py       # Browser lifecycle
│   ├── context_fixtures.py       # Context & page per test
│   ├── auth_fixtures.py          # Auth orchestration
│   ├── api_fixtures.py           # API client fixtures
│   └── data_fixtures.py          # Test data setup/cleanup
│
├── pages/                         # Page Object Model
│   ├── base_page.py              # Shared UI utilities
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── user_management_page.py
│
├── data/                          # Test data
│   ├── test_users.json
│   ├── test_payloads.json
│   └── expected_responses.json
│
├── utils/                         # Utilities
│   ├── logger.py                 # Centralized logging
│   ├── assertions.py             # Assertion helpers
│   └── data_loader.py            # Data loading utilities
│
├── tests/                         # Tests
│   ├── smoke/                    # Smoke tests
│   ├── sanity/                   # Sanity tests
│   └── regression/               # Regression tests
│
├── ci/                            # CI scripts
│   ├── run_smoke.sh
│   ├── run_sanity.sh
│   └── run_regression.sh
│
└── reports/                       # Generated reports
    ├── allure-results/
    └── html-report/
```

## 🔑 Key Principles

1. **Core defines capabilities, Fixtures orchestrate lifecycle**
   - Core layer knows *how* to do things
   - Fixtures decide *when* to do them

2. **Tests are thin**
   - Only business validation
   - Zero infrastructure logic

3. **Configuration flows down**
   - Centrally resolved
   - Injected via fixtures

4. **Authentication is reusable**
   - Persisted and validated
   - Never repeated unnecessarily

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
playwright install chromium
```

### Environment Setup

Set environment variables for credentials:

```bash
export QA_USERNAME="your_username"
export QA_PASSWORD="your_password"
```

### Run Tests

**Smoke tests (quick validation):**
```bash
pytest -m smoke -v
# or
./ci/run_smoke.sh
```

**Sanity tests (feature validation):**
```bash
pytest -m sanity -v
# or
./ci/run_sanity.sh
```

**Regression tests (comprehensive):**
```bash
pytest -m regression -v
# or
./ci/run_regression.sh
```

**Run specific environment:**
```bash
pytest --env=staging -m smoke
```

**Run specific browser:**
```bash
pytest --browser-type=firefox --headless
```

## 📊 Reports

### Generate Allure Report

```bash
allure serve reports/allure-results
```

### HTML Report

Generated automatically at: `reports/html-report/report.html`

## 🎨 Framework Highlights

### 1. Execution Entry Point

**pytest.ini** and **conftest.py** establish:
- Registered markers (smoke, sanity, regression)
- CLI options (--env, --browser-type, --headless)
- Global execution behavior

### 2. Configuration Layer

**config/** manages all environment and execution settings:
- Environment-specific URLs and credentials
- Browser configuration
- Timeouts and retries
- Feature flags

### 3. Core Infrastructure

**core/** defines capabilities:
- **BrowserManager**: How to launch browsers
- **ContextManager**: How to create isolated contexts
- **AuthManager**: How to authenticate and validate

### 4. Fixtures Orchestration

**fixtures/** controls lifecycle:
- Browser lifecycle (session scope)
- Context & page per test (function scope)
- Authentication reuse
- API client provisioning

### 5. Page Object Model

**pages/** separates UI from tests:
- Business-level methods
- No selectors in tests
- Centralized UI changes

### 6. Dual-Layer Testing

- **UI tests**: Via Page Objects
- **API tests**: Via API clients
- **Hybrid**: Create via UI, validate via API

## 🎯 Interview Talking Points

### Layer 1: Foundation
*"I start with pytest.ini and conftest.py because these define how the framework behaves before any test runs. pytest.ini establishes execution contracts with markers and defaults, while conftest.py orchestrates fixture registration and global hooks."*

### Layer 2: Configuration
*"Configuration is resolved centrally through config_loader, which merges YAML files, environment variables, and CLI arguments. Tests never know which environment they run against—configuration flows down via fixtures."*

### Layer 3: Core Infrastructure
*"The core layer defines execution capabilities but doesn't control timing. BrowserManager knows how to launch browsers, ContextManager knows how to create contexts, AuthManager knows how to authenticate—but fixtures decide when these happen."*

### Layer 4: Fixtures
*"Fixtures are the glue between pytest and core infrastructure. They control lifecycle, orchestration, and dependency injection. Tests remain clean because all setup complexity lives here."*

### Layer 5: Tests
*"Tests are intentionally thin—just business validation. They never handle authentication, environment management, retries, or UI implementation. Everything delegates to fixtures and abstraction layers."*

## 📝 Development Guidelines

1. **Never hardcode configuration** - Use config_loader
2. **Keep tests thin** - Delegate to page objects and fixtures
3. **One assertion focus per test** - Clear failure diagnosis
4. **Use markers consistently** - smoke, sanity, regression
5. **Clean up after tests** - Use cleanup fixtures

## 🔧 Extending the Framework

### Add new page object:

```python
from pages.base_page import BasePage

class NewPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page)
        self.url = f"{base_url}/new-page"
```

### Add new API endpoint:

```python
class NewAPI:
    def __init__(self, client):
        self.client = client
    
    def new_operation(self, data):
        return self.client.post("/endpoint", json=data)
```

### Add new test:

```python
@pytest.mark.smoke
def test_new_feature(page, config):
    # Test logic using fixtures
    pass
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [Allure Reporting](https://docs.qameta.io/allure/)

---

**Built for interview demonstration** | **Production-ready architecture** | **Enterprise-scale testing**

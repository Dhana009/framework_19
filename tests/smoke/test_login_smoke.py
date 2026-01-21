"""
Smoke Test - Login

Validates critical login functionality.

Purpose:
- Verify valid login works
- Quick validation of core auth flow

Scope: Smoke test
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_loader import get_data_loader


@pytest.mark.smoke
@pytest.mark.ui
def test_valid_login(unauthenticated_page, config):
    """
    Test successful login with valid credentials.
    
    This is a smoke test - validates the most critical path.
    """
    # Arrange
    data_loader = get_data_loader()
    credentials = data_loader.get_test_user("valid_user")
    
    login_page = LoginPage(unauthenticated_page, config.ui_base_url)
    dashboard_page = DashboardPage(unauthenticated_page, config.ui_base_url)
    
    # Act
    login_page.goto()
    login_page.login(credentials["email"], credentials["password"])
    
    # Assert
    assert login_page.is_login_successful(), "Login should redirect away from login page"
    assert dashboard_page.is_loaded(), "Dashboard should load after successful login"


@pytest.mark.smoke
@pytest.mark.ui
def test_invalid_login(unauthenticated_page, config):
    """
    Test login failure with invalid credentials.
    
    Validates that invalid credentials are properly rejected.
    """
    # Arrange
    data_loader = get_data_loader()
    credentials = data_loader.get_test_user("invalid_user")
    
    login_page = LoginPage(unauthenticated_page, config.ui_base_url)
    
    # Act
    login_page.goto()
    login_page.login(credentials["email"], credentials["password"])
    
    # Assert
    assert not login_page.is_login_successful(), "Login should fail with invalid credentials"
    error_message = login_page.get_error_message()
    assert error_message, "Error message should be displayed"

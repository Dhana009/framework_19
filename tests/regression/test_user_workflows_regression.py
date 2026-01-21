"""
Regression Test - User Workflows

Comprehensive end-to-end user workflow validation.

Purpose:
- Test complete user lifecycle
- Validate complex workflows
- Ensure all features work together

Scope: Regression test
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.user_management_page import UserManagementPage
from utils.assertions import assert_url_contains
import time


@pytest.mark.regression
@pytest.mark.ui
def test_complete_user_workflow(unauthenticated_page, config):
    """
    Test complete user workflow: Login -> Navigate -> Manage Users -> Logout.
    
    This is a comprehensive end-to-end test.
    """
    # Arrange
    credentials = {
        "email": "admin@example.com",
        "password": "Admin@12345"
    }
    
    login_page = LoginPage(unauthenticated_page, config.ui_base_url)
    dashboard_page = DashboardPage(unauthenticated_page, config.ui_base_url)
    user_mgmt_page = UserManagementPage(unauthenticated_page, config.ui_base_url)
    
    # Act & Assert - Step 1: Login
    login_page.goto()
    login_page.login(credentials["email"], credentials["password"])
    assert login_page.is_login_successful(), "Login should succeed"
    
    # Step 2: Verify dashboard loads
    assert dashboard_page.is_loaded(), "Dashboard should load"
    
    # Step 3: Navigate to User Management
    dashboard_page.navigate_to_user_management()
    assert user_mgmt_page.is_loaded(), "User management page should load"
    
    # Step 4: Verify user list is visible
    assert_url_contains(unauthenticated_page, "/users")
    
    # Step 5: Logout
    dashboard_page.goto()
    dashboard_page.logout()
    
    # Verify redirected to login
    assert "/login" in unauthenticated_page.url.lower(), "Should redirect to login after logout"


@pytest.mark.regression
@pytest.mark.api
def test_user_api_crud_workflow(user_api, cleanup_created_users):
    """
    Test complete CRUD workflow via API.
    
    Create -> Read -> Update -> Delete user via API.
    """
    # Note: This is a demonstration structure
    # In real implementation:
    
    # 1. Create user via API
    user_data = {
        "email": f"apiuser_{int(time.time())}@example.com",
        "password": "ApiUser@123",
        "name": "API Test User",
        "role": "user"
    }
    
    # created_user = user_api.create_user(user_data)
    # cleanup_created_users.append(created_user["id"])
    
    # 2. Read user
    # fetched_user = user_api.get_user(created_user["id"])
    # assert fetched_user["email"] == user_data["email"]
    
    # 3. Update user
    # updated_user = user_api.update_user(created_user["id"], {"name": "Updated Name"})
    # assert updated_user["name"] == "Updated Name"
    
    # 4. Delete user (or let cleanup fixture handle it)
    
    print("\n✓ API CRUD workflow would execute here")
    pytest.skip("Demo test - requires backend integration")

"""
Data Fixtures

Handles test data setup and cleanup.

Responsibilities:
- Seed test data before tests
- Cleanup test data after tests
- Ensure test independence
"""

import pytest
from typing import Dict, Any


@pytest.fixture(scope="function")
def test_user_data():
    """
    Provide test user data for user creation tests.
    
    Scope: function (fresh data per test)
    """
    return {
        "email": f"testuser_{pytest.timestamp}@example.com",
        "password": "Test@12345",
        "name": "Test User",
        "role": "user"
    }


@pytest.fixture(scope="function")
def cleanup_created_users(user_api):
    """
    Cleanup users created during test.
    
    Usage in test:
        def test_something(cleanup_created_users):
            user = create_user(...)
            cleanup_created_users.append(user["id"])
            # user will be deleted after test
    
    Scope: function
    """
    created_user_ids = []
    
    yield created_user_ids
    
    # Cleanup after test
    for user_id in created_user_ids:
        try:
            user_api.delete_user(user_id)
            print(f"Cleaned up user: {user_id}")
        except Exception as e:
            print(f"Failed to cleanup user {user_id}: {e}")


@pytest.fixture(scope="session", autouse=True)
def setup_test_data(user_api):
    """
    Set up baseline test data at session start.
    
    This runs automatically before any tests.
    
    Scope: session, autouse
    """
    print("\nSetting up baseline test data...")
    
    # In real implementation, seed required baseline data
    # For example:
    # - Create admin user
    # - Create test roles
    # - Seed reference data
    
    yield
    
    # Cleanup after session
    print("\nCleaning up baseline test data...")


# Add timestamp to pytest for unique test data generation
def pytest_configure(config):
    """Add timestamp to pytest"""
    import time
    pytest.timestamp = int(time.time())

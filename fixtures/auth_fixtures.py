"""
Authentication Fixtures

Orchestrates authentication lifecycle.

Responsibilities:
- Check if valid auth exists
- Validate auth state
- Re-authenticate only when needed
- Provide storage state to context fixtures

Uses auth_manager for authentication mechanics.
"""

import pytest
from core.auth_manager import AuthManager


@pytest.fixture(scope="session")
def auth_manager(config):
    """
    Provide AuthManager instance.
    
    Scope: session
    """
    auth_config = config.auth_config
    return AuthManager(auth_config)


@pytest.fixture(scope="session")
def auth_state(auth_manager, config):
    """
    Provide valid authentication storage state.
    
    This fixture orchestrates the authentication lifecycle:
    1. Check if valid auth state exists
    2. If not, authenticate and persist state
    3. Return path to storage state
    
    Scope: session (auth is reused across all tests)
    """
    # Check if we have valid storage state
    storage_state_path = auth_manager.get_storage_state_path()
    
    if storage_state_path:
        print("\nReusing existing authentication state")
        return storage_state_path
    
    print("\nNo valid authentication found - would authenticate here")
    print("Note: In real implementation, this would call auth_manager.authenticate_via_ui()")
    print("      or auth_manager.authenticate_via_api() and generate storage_state.json")
    
    # For demo purposes, we return None (no auth)
    # In real implementation:
    # 1. Get credentials from config
    # 2. Authenticate via UI or API
    # 3. Return storage_state_path
    
    return None


@pytest.fixture(scope="function")
def fresh_auth(auth_manager, config):
    """
    Force fresh authentication (ignore cached state).
    
    Use this fixture when tests specifically need to test login flow.
    
    Scope: function
    """
    # Clear existing auth
    auth_manager.clear_storage_state()
    
    print("\nForced fresh authentication")
    
    # Authenticate
    # (In real implementation, perform actual auth here)
    
    return None

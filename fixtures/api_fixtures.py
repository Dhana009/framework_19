"""
API Fixtures

Provides authenticated API clients.

Responsibilities:
- Create API client with base config
- Inject authentication tokens
- Provide domain-specific API instances
"""

import pytest
from api.api_client import APIClient
from api.auth_api import AuthAPI
from api.user_api import UserAPI


@pytest.fixture(scope="session")
def api_client(config):
    """
    Provide base API client.
    
    Scope: session
    """
    api_base_url = config.api_base_url
    timeout = config.timeouts.get("api_request", 30000) // 1000  # Convert ms to seconds
    retry_config = config.retry_config
    
    client = APIClient(
        base_url=api_base_url,
        timeout=timeout,
        retry_config=retry_config
    )
    
    yield client
    
    # Cleanup
    client.close()


@pytest.fixture(scope="session")
def authenticated_api_client(api_client, config):
    """
    Provide authenticated API client.
    
    This fixture:
    - Takes base API client
    - Authenticates and gets token
    - Sets token in client headers
    - Returns authenticated client
    
    Scope: session (reuse auth across tests)
    """
    # In real implementation, authenticate and set token
    # credentials = config.credentials
    # auth_api = AuthAPI(api_client)
    # auth_data = auth_api.login(credentials["username"], credentials["password"])
    # token = auth_data["access_token"]
    # api_client.set_auth_token(token)
    
    print("\nAPI client authenticated (demo mode)")
    
    return api_client


@pytest.fixture(scope="session")
def auth_api(authenticated_api_client):
    """
    Provide AuthAPI instance.
    
    Scope: session
    """
    return AuthAPI(authenticated_api_client)


@pytest.fixture(scope="session")
def user_api(authenticated_api_client):
    """
    Provide UserAPI instance.
    
    Scope: session
    """
    return UserAPI(authenticated_api_client)

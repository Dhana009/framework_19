"""
Data Loader

Utilities for loading test data from files.

Responsibilities:
- Load JSON/YAML files
- Parse and validate data
- Provide structured data objects
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List


class DataLoader:
    """
    Load and parse test data files.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data loader.
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """
        Load JSON file.
        
        Args:
            filename: JSON file name (with or without .json extension)
        
        Returns:
            Parsed JSON as dict
        """
        if not filename.endswith(".json"):
            filename = f"{filename}.json"
        
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load YAML file.
        
        Args:
            filename: YAML file name (with or without .yaml/.yml extension)
        
        Returns:
            Parsed YAML as dict
        """
        if not (filename.endswith(".yaml") or filename.endswith(".yml")):
            filename = f"{filename}.yaml"
        
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    def get_test_user(self, user_type: str = "valid_user") -> Dict[str, str]:
        """
        Get test user credentials.
        
        Args:
            user_type: Type of user (valid_user, admin_user, etc.)
        
        Returns:
            User credentials dict
        """
        users = self.load_json("test_users")
        
        if user_type not in users:
            raise ValueError(f"User type '{user_type}' not found in test_users.json")
        
        return users[user_type]
    
    def get_test_payload(self, payload_name: str) -> Dict[str, Any]:
        """
        Get test API payload.
        
        Args:
            payload_name: Payload name
        
        Returns:
            Payload dict
        """
        payloads = self.load_json("test_payloads")
        
        if payload_name not in payloads:
            raise ValueError(f"Payload '{payload_name}' not found in test_payloads.json")
        
        return payloads[payload_name]
    
    def get_expected_response(self, response_name: str) -> Dict[str, Any]:
        """
        Get expected API response.
        
        Args:
            response_name: Response name
        
        Returns:
            Expected response dict
        """
        responses = self.load_json("expected_responses")
        
        if response_name not in responses:
            raise ValueError(f"Response '{response_name}' not found in expected_responses.json")
        
        return responses[response_name]


# Global instance for convenience
_default_loader = None


def get_data_loader() -> DataLoader:
    """Get global DataLoader instance"""
    global _default_loader
    if _default_loader is None:
        _default_loader = DataLoader()
    return _default_loader

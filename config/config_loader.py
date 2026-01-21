"""
Configuration Loader

Responsible for:
- Loading YAML configuration files
- Resolving environment variables
- Merging CLI arguments
- Exposing unified configuration object

The config loader is the single source of truth for all configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from string import Template


class ConfigLoader:
    """
    Central configuration management.
    
    Resolution order:
    1. Load base config files (env_config.yaml, test_config.yaml)
    2. Resolve environment variables
    3. Override with CLI arguments
    """
    
    def __init__(self, env: str = "qa", cli_options: Dict[str, Any] = None):
        """
        Initialize configuration loader.
        
        Args:
            env: Environment name (qa, staging, production)
            cli_options: Dictionary of CLI options to override config
        """
        self.env = env
        self.cli_options = cli_options or {}
        self.config_dir = Path(__file__).parent
        
        # Load configurations
        self._env_config = self._load_env_config()
        self._test_config = self._load_test_config()
        
        # Apply overrides
        self._apply_cli_overrides()
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load and parse YAML file"""
        filepath = self.config_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    def _resolve_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively resolve environment variables in config.
        
        Replaces ${VAR_NAME} with actual environment variable value.
        """
        if isinstance(config, dict):
            return {k: self._resolve_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            # Extract variable name
            var_name = config[2:-1]
            # Return env var value or original if not found
            return os.getenv(var_name, config)
        else:
            return config
    
    def _load_env_config(self) -> Dict[str, Any]:
        """Load environment-specific configuration"""
        all_env_config = self._load_yaml("env_config.yaml")
        
        if self.env not in all_env_config:
            raise ValueError(f"Environment '{self.env}' not found in env_config.yaml")
        
        env_config = all_env_config[self.env]
        return self._resolve_env_vars(env_config)
    
    def _load_test_config(self) -> Dict[str, Any]:
        """Load test execution configuration"""
        test_config = self._load_yaml("test_config.yaml")
        return self._resolve_env_vars(test_config)
    
    def _apply_cli_overrides(self):
        """Apply CLI options to override config values"""
        # Override browser type if provided
        if "browser_type" in self.cli_options:
            self._test_config["browser"]["type"] = self.cli_options["browser_type"]
        
        # Override headless mode if provided
        if "headless" in self.cli_options:
            self._test_config["browser"]["headless"] = self.cli_options["headless"]
    
    # ========================================================================
    # PUBLIC API - Expose configuration values
    # ========================================================================
    
    @property
    def ui_base_url(self) -> str:
        """Get UI base URL for current environment"""
        return self._env_config["ui"]["base_url"]
    
    @property
    def api_base_url(self) -> str:
        """Get API base URL for current environment"""
        return self._env_config["api"]["base_url"]
    
    @property
    def credentials(self) -> Dict[str, str]:
        """Get credentials for current environment"""
        return self._env_config["credentials"]
    
    @property
    def features(self) -> Dict[str, bool]:
        """Get feature flags for current environment"""
        return self._env_config.get("features", {})
    
    @property
    def browser_config(self) -> Dict[str, Any]:
        """Get browser configuration"""
        return self._test_config["browser"]
    
    @property
    def timeouts(self) -> Dict[str, int]:
        """Get timeout configuration"""
        return self._test_config["timeouts"]
    
    @property
    def retry_config(self) -> Dict[str, Any]:
        """Get retry configuration"""
        return self._test_config["retry"]
    
    @property
    def logging_config(self) -> Dict[str, str]:
        """Get logging configuration"""
        return self._test_config["logging"]
    
    @property
    def screenshot_config(self) -> Dict[str, Any]:
        """Get screenshot configuration"""
        return self._test_config["screenshots"]
    
    @property
    def video_config(self) -> Dict[str, Any]:
        """Get video configuration"""
        return self._test_config["video"]
    
    @property
    def auth_config(self) -> Dict[str, Any]:
        """Get authentication configuration"""
        return self._test_config["authentication"]
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get any configuration value by dot notation.
        
        Example:
            config.get("browser.viewport.width")
        """
        keys = key.split(".")
        
        # Try test_config first
        value = self._test_config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Try env_config
                value = self._env_config
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        return default
                return value
        return value


# ============================================================================
# PYTEST INTEGRATION
# ============================================================================

def get_config(request) -> ConfigLoader:
    """
    Create ConfigLoader from pytest request.
    
    This function is meant to be used in fixtures.
    """
    env = request.config.getoption("--env")
    browser_type = request.config.getoption("--browser-type")
    headless = request.config.getoption("--headless")
    
    cli_options = {
        "browser_type": browser_type,
        "headless": headless,
    }
    
    return ConfigLoader(env=env, cli_options=cli_options)

"""
Configuration Management

Loads and manages configuration from YAML files.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        path: Path to the YAML configuration file (default: "config.yaml")
    
    Returns:
        Dictionary containing configuration parameters
    
    Raises:
        FileNotFoundError: If the config file doesn't exist
        yaml.YAMLError: If the YAML file is malformed
    
    Examples:
        >>> config = load_config("config.yaml")
        >>> print(config["seed"])
        42
    """
    config_path = Path(path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML configuration: {e}")
    
    # Validate required keys
    required_keys = ["seed", "device", "paths"]
    missing_keys = [key for key in required_keys if key not in config]
    
    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {missing_keys}")
    
    # Expand paths to absolute paths
    if "paths" in config:
        for key, value in config["paths"].items():
            if isinstance(value, str):
                config["paths"][key] = str(Path(value).resolve())
    
    return config


def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get a nested configuration value using dot notation.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the key (e.g., "paths.data_dir")
        default: Default value if key not found
    
    Returns:
        Configuration value or default
    
    Examples:
        >>> config = {"paths": {"data_dir": "/data"}}
        >>> get_config_value(config, "paths.data_dir")
        '/data'
        >>> get_config_value(config, "paths.missing", default="default")
        'default'
    """
    keys = key_path.split(".")
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def save_config(config: Dict[str, Any], path: str = "config.yaml") -> None:
    """
    Save configuration to a YAML file.
    
    Args:
        config: Configuration dictionary to save
        path: Path where to save the configuration
    
    Examples:
        >>> config = {"seed": 42, "device": "cuda"}
        >>> save_config(config, "my_config.yaml")
    """
    config_path = Path(path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


# Global configuration instance (loaded lazily)
_global_config: Optional[Dict[str, Any]] = None


def get_global_config(reload: bool = False) -> Dict[str, Any]:
    """
    Get the global configuration instance (singleton pattern).
    
    Args:
        reload: If True, reload the configuration from disk
    
    Returns:
        Global configuration dictionary
    """
    global _global_config
    
    if _global_config is None or reload:
        _global_config = load_config()
    
    return _global_config

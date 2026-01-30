"""
Unit tests for configuration management
"""

import pytest
import tempfile
from pathlib import Path
import yaml

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agi_core.config import (
    load_config,
    get_config_value,
    save_config,
    get_global_config
)


class TestConfigLoading:
    """Tests for configuration loading functionality"""
    
    def test_load_config_success(self, tmp_path):
        """Test successful configuration loading"""
        config_data = {
            "seed": 42,
            "device": "cuda",
            "paths": {
                "data_dir": "data",
                "models_dir": "models"
            }
        }
        
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        config = load_config(str(config_file))
        
        assert config["seed"] == 42
        assert config["device"] == "cuda"
        assert "paths" in config
        assert "data_dir" in config["paths"]
    
    def test_load_config_file_not_found(self):
        """Test error when config file doesn't exist"""
        with pytest.raises(FileNotFoundError):
            load_config("nonexistent_config.yaml")
    
    def test_load_config_missing_required_keys(self, tmp_path):
        """Test error when required keys are missing"""
        config_data = {"device": "cuda"}  # Missing 'seed' and 'paths'
        
        config_file = tmp_path / "incomplete_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        with pytest.raises(ValueError):
            load_config(str(config_file))
    
    def test_load_config_malformed_yaml(self, tmp_path):
        """Test error with malformed YAML"""
        config_file = tmp_path / "bad_config.yaml"
        with open(config_file, 'w') as f:
            f.write("invalid: yaml: content:")
        
        with pytest.raises(yaml.YAMLError):
            load_config(str(config_file))


class TestConfigUtilities:
    """Tests for configuration utility functions"""
    
    def test_get_config_value_simple(self):
        """Test getting simple config value"""
        config = {"seed": 42, "device": "cuda"}
        
        assert get_config_value(config, "seed") == 42
        assert get_config_value(config, "device") == "cuda"
    
    def test_get_config_value_nested(self):
        """Test getting nested config value"""
        config = {
            "paths": {
                "data_dir": "/data",
                "models": {
                    "checkpoint_dir": "/models/checkpoints"
                }
            }
        }
        
        assert get_config_value(config, "paths.data_dir") == "/data"
        assert get_config_value(config, "paths.models.checkpoint_dir") == "/models/checkpoints"
    
    def test_get_config_value_default(self):
        """Test default value when key not found"""
        config = {"seed": 42}
        
        assert get_config_value(config, "missing_key", default="default") == "default"
        assert get_config_value(config, "paths.missing", default=None) is None
    
    def test_save_config(self, tmp_path):
        """Test saving configuration to file"""
        config = {"seed": 42, "device": "cuda"}
        config_file = tmp_path / "saved_config.yaml"
        
        save_config(config, str(config_file))
        
        assert config_file.exists()
        
        # Load it back and verify
        with open(config_file, 'r') as f:
            loaded = yaml.safe_load(f)
        
        assert loaded["seed"] == 42
        assert loaded["device"] == "cuda"


class TestGlobalConfig:
    """Tests for global configuration management"""
    
    def test_get_global_config(self, monkeypatch, tmp_path):
        """Test global config singleton"""
        # Create a test config
        config_data = {
            "seed": 99,
            "device": "cpu",
            "paths": {
                "data_dir": "test_data"
            }
        }
        
        config_file = tmp_path / "global_test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        # Change working directory to tmp_path
        monkeypatch.chdir(tmp_path)
        
        # Rename to config.yaml (default name)
        config_file.rename(tmp_path / "config.yaml")
        
        # Get global config
        config = get_global_config()
        
        assert config["seed"] == 99
        assert config["device"] == "cpu"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

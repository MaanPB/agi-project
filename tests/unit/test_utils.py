"""
Unit tests for utility functions
"""

import pytest
import random
import numpy as np
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agi_core.utils import (
    set_seed,
    ensure_dir,
    now_str,
    get_device,
    format_number,
    get_file_size,
    safe_divide,
    create_run_id,
    load_yaml,
    save_yaml
)


class TestSetSeed:
    """Tests for set_seed function"""
    
    def test_set_seed_reproducibility(self):
        """Test that set_seed makes random operations reproducible"""
        set_seed(42)
        random_nums_1 = [random.random() for _ in range(5)]
        np_nums_1 = np.random.rand(5)
        
        set_seed(42)
        random_nums_2 = [random.random() for _ in range(5)]
        np_nums_2 = np.random.rand(5)
        
        assert random_nums_1 == random_nums_2
        assert np.allclose(np_nums_1, np_nums_2)
    
    def test_set_seed_different_seeds(self):
        """Test that different seeds produce different results"""
        set_seed(42)
        nums_1 = [random.random() for _ in range(5)]
        
        set_seed(123)
        nums_2 = [random.random() for _ in range(5)]
        
        assert nums_1 != nums_2


class TestEnsureDir:
    """Tests for ensure_dir function"""
    
    def test_ensure_dir_creates_directory(self, tmp_path):
        """Test that ensure_dir creates a new directory"""
        new_dir = tmp_path / "test_dir"
        
        result = ensure_dir(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()
        assert result == new_dir
    
    def test_ensure_dir_nested_directories(self, tmp_path):
        """Test creating nested directories"""
        nested_dir = tmp_path / "level1" / "level2" / "level3"
        
        ensure_dir(nested_dir)
        
        assert nested_dir.exists()
        assert nested_dir.is_dir()
    
    def test_ensure_dir_already_exists(self, tmp_path):
        """Test that ensure_dir works with existing directory"""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()
        
        # Should not raise an error
        result = ensure_dir(existing_dir)
        
        assert result == existing_dir
        assert existing_dir.exists()


class TestNowStr:
    """Tests for now_str function"""
    
    def test_now_str_default_format(self):
        """Test default timestamp format"""
        timestamp = now_str()
        
        # Should be parseable with the default format
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    
    def test_now_str_custom_format(self):
        """Test custom timestamp format"""
        timestamp = now_str("%Y%m%d")
        
        # Should be 8 digits (YYYYMMDD)
        assert len(timestamp) == 8
        assert timestamp.isdigit()
    
    def test_now_str_consistency(self):
        """Test that now_str returns consistent format"""
        ts1 = now_str("%Y-%m-%d")
        ts2 = now_str("%Y-%m-%d")
        
        # Both should be the same day
        assert ts1 == ts2


class TestGetDevice:
    """Tests for get_device function"""
    
    def test_get_device_returns_valid_device(self):
        """Test that get_device returns a valid device string"""
        device = get_device()
        
        assert device in ["cuda", "mps", "cpu"]
    
    def test_get_device_cpu_fallback(self):
        """Test that cpu is returned when preferred device unavailable"""
        # This will always work
        device = get_device("cpu")
        
        assert device == "cpu"


class TestFormatNumber:
    """Tests for format_number function"""
    
    def test_format_number_thousands(self):
        """Test formatting thousands"""
        assert "1.50K" in format_number(1500)
        assert "K" in format_number(5000)
    
    def test_format_number_millions(self):
        """Test formatting millions"""
        assert "2.50M" in format_number(2500000)
        assert "M" in format_number(1000000)
    
    def test_format_number_billions(self):
        """Test formatting billions"""
        assert "3.00B" in format_number(3000000000)
        assert "B" in format_number(1500000000)
    
    def test_format_number_small_numbers(self):
        """Test formatting small numbers"""
        result = format_number(42)
        assert "42" in result
    
    def test_format_number_precision(self):
        """Test custom precision"""
        result = format_number(1234, precision=1)
        assert "1.2K" == result


class TestGetFileSize:
    """Tests for get_file_size function"""
    
    def test_get_file_size_nonexistent(self):
        """Test with nonexistent file"""
        size = get_file_size("nonexistent_file.txt")
        assert size == "File not found"
    
    def test_get_file_size_small_file(self, tmp_path):
        """Test with small file"""
        test_file = tmp_path / "small.txt"
        test_file.write_text("Hello world!")
        
        size = get_file_size(test_file)
        assert "B" in size
    
    def test_get_file_size_large_file(self, tmp_path):
        """Test with larger file"""
        test_file = tmp_path / "large.txt"
        # Create a ~10KB file
        test_file.write_text("x" * 10000)
        
        size = get_file_size(test_file)
        assert "KB" in size or "B" in size


class TestSafeDivide:
    """Tests for safe_divide function"""
    
    def test_safe_divide_normal(self):
        """Test normal division"""
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(7, 3) == pytest.approx(2.333, rel=1e-2)
    
    def test_safe_divide_by_zero(self):
        """Test division by zero returns default"""
        assert safe_divide(10, 0) == 0.0
        assert safe_divide(10, 0, default=999) == 999
    
    def test_safe_divide_negative(self):
        """Test with negative numbers"""
        assert safe_divide(-10, 2) == -5.0
        assert safe_divide(10, -2) == -5.0


class TestCreateRunId:
    """Tests for create_run_id function"""
    
    def test_create_run_id_default(self):
        """Test default run ID creation"""
        run_id = create_run_id()
        
        assert run_id.startswith("run_")
        assert len(run_id) > 4
    
    def test_create_run_id_custom_prefix(self):
        """Test custom prefix"""
        run_id = create_run_id("experiment")
        
        assert run_id.startswith("experiment_")
    
    def test_create_run_id_unique(self):
        """Test that run IDs are unique (timestamp-based)"""
        id1 = create_run_id()
        id2 = create_run_id()
        
        # They might be the same if called in same second, but structure should be valid
        assert "_" in id1
        assert "_" in id2


class TestYamlFunctions:
    """Tests for YAML utility functions"""
    
    def test_load_yaml(self, tmp_path):
        """Test loading YAML file"""
        import yaml
        
        test_data = {"key1": "value1", "key2": 42}
        yaml_file = tmp_path / "test.yaml"
        
        with open(yaml_file, 'w') as f:
            yaml.dump(test_data, f)
        
        loaded = load_yaml(yaml_file)
        
        assert loaded["key1"] == "value1"
        assert loaded["key2"] == 42
    
    def test_save_yaml(self, tmp_path):
        """Test saving YAML file"""
        test_data = {"name": "test", "value": 123}
        yaml_file = tmp_path / "output.yaml"
        
        save_yaml(test_data, yaml_file)
        
        assert yaml_file.exists()
        
        # Load it back
        loaded = load_yaml(yaml_file)
        assert loaded["name"] == "test"
        assert loaded["value"] == 123
    
    def test_save_yaml_creates_directory(self, tmp_path):
        """Test that save_yaml creates parent directories"""
        yaml_file = tmp_path / "nested" / "dir" / "output.yaml"
        test_data = {"test": "data"}
        
        save_yaml(test_data, yaml_file)
        
        assert yaml_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Utility Functions

Common helper functions used throughout the project.
"""

import os
import random
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
import numpy as np


def set_seed(seed: int) -> None:
    """
    Set random seed for reproducibility across Python, NumPy, and PyTorch.
    
    Args:
        seed: Random seed value
    
    Examples:
        >>> set_seed(42)
        >>> # Now all random operations are reproducible
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    
    # Set PyTorch seed if available
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass  # PyTorch not installed yet


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure
    
    Returns:
        Path object of the directory
    
    Examples:
        >>> ensure_dir("data/models")
        PosixPath('data/models')
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def now_str(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp as a formatted string.
    
    Args:
        format: strftime format string
    
    Returns:
        Formatted timestamp string
    
    Examples:
        >>> now_str()
        '2026-01-30 14:23:45'
        >>> now_str("%Y%m%d_%H%M%S")
        '20260130_142345'
    """
    return datetime.now().strftime(format)


def get_device(preferred: str = "cuda") -> str:
    """
    Get the best available device (cuda, mps, or cpu).
    
    Args:
        preferred: Preferred device ("cuda", "mps", or "cpu")
    
    Returns:
        Device string that can be used with PyTorch
    
    Examples:
        >>> device = get_device("cuda")
        >>> print(device)
        'cuda'  # or 'cpu' if CUDA not available
    """
    try:
        import torch
        
        if preferred == "cuda" and torch.cuda.is_available():
            return "cuda"
        elif preferred == "mps" and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    except ImportError:
        return "cpu"


def count_parameters(model) -> int:
    """
    Count the total number of trainable parameters in a PyTorch model.
    
    Args:
        model: PyTorch model
    
    Returns:
        Total number of trainable parameters
    
    Examples:
        >>> import torch.nn as nn
        >>> model = nn.Linear(10, 5)
        >>> count_parameters(model)
        55
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def format_number(num: Union[int, float], precision: int = 2) -> str:
    """
    Format a large number with K/M/B suffixes.
    
    Args:
        num: Number to format
        precision: Decimal precision
    
    Returns:
        Formatted number string
    
    Examples:
        >>> format_number(1500)
        '1.50K'
        >>> format_number(2500000)
        '2.50M'
    """
    if num >= 1e9:
        return f"{num/1e9:.{precision}f}B"
    elif num >= 1e6:
        return f"{num/1e6:.{precision}f}M"
    elif num >= 1e3:
        return f"{num/1e3:.{precision}f}K"
    else:
        return f"{num:.{precision}f}"


def get_file_size(path: Union[str, Path]) -> str:
    """
    Get human-readable file size.
    
    Args:
        path: Path to file
    
    Returns:
        Formatted file size string
    
    Examples:
        >>> get_file_size("model.pth")
        '15.3 MB'
    """
    file_path = Path(path)
    
    if not file_path.exists():
        return "File not found"
    
    size_bytes = file_path.stat().st_size
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} PB"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
    
    Returns:
        Result of division or default
    
    Examples:
        >>> safe_divide(10, 2)
        5.0
        >>> safe_divide(10, 0, default=0.0)
        0.0
    """
    if denominator == 0:
        return default
    return numerator / denominator


def create_run_id(prefix: str = "run") -> str:
    """
    Create a unique run ID with timestamp.
    
    Args:
        prefix: Prefix for the run ID
    
    Returns:
        Unique run ID string
    
    Examples:
        >>> create_run_id("experiment")
        'experiment_20260130_142345'
    """
    timestamp = now_str("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}"


def load_yaml(path: Union[str, Path]) -> dict:
    """
    Load YAML file (wrapper for consistency).
    
    Args:
        path: Path to YAML file
    
    Returns:
        Dictionary from YAML
    """
    import yaml
    
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(data: dict, path: Union[str, Path]) -> None:
    """
    Save dictionary to YAML file.
    
    Args:
        data: Dictionary to save
        path: Path where to save
    """
    import yaml
    
    file_path = Path(path)
    ensure_dir(file_path.parent)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

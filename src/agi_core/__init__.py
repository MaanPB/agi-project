"""
AGI Core Module

A modular AI system with retrieval, tools, planning, memory, and continual learning.
"""

__version__ = "0.1.0"
__author__ = "AGI Project Team"

from .config import load_config
from .logger import get_logger
from .utils import set_seed, ensure_dir, now_str

__all__ = [
    "load_config",
    "get_logger",
    "set_seed",
    "ensure_dir",
    "now_str",
]

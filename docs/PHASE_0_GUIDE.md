# Phase 0 - Quick Start Guide

## 🎉 Congratulations! Phase 0 is Complete

You now have a fully functional foundation for the AGI project with:
- ✅ Project structure
- ✅ Configuration management
- ✅ Structured logging
- ✅ Utility functions
- ✅ Unit tests

## 📋 What You Just Built

### Core Modules

1. **config.py** - Configuration management
   - Load/save YAML configs
   - Nested config access
   - Global config singleton

2. **logger.py** - Structured JSON logging
   - JSON formatted logs
   - Correlation IDs for tracking
   - Context loggers with extra fields

3. **utils.py** - Common utilities
   - Seed setting for reproducibility
   - Directory management
   - Number formatting
   - File operations

4. **main.py** - Entry point
   - Demonstrates all components working together

### Tests

- **test_config.py** - 10+ tests for configuration
- **test_logger.py** - 10+ tests for logging
- **test_utils.py** - 15+ tests for utilities

## 🚀 How to Run

### 1. Set up your environment

```bash
cd agi_project

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the demo

```bash
python -m src.agi_core.main
```

You should see:
```
============================================================
AGI Core System - Phase 0 Verification
============================================================

📋 Loading configuration...
✅ Configuration loaded successfully!
   - Seed: 42
   - Device: cuda
   - Log level: INFO

🎲 Setting random seed...
✅ Random seed set to 42

📝 Initializing logger...
✅ Logger initialized successfully!

📁 Creating project directories...
✅ Created 6 directories:
   - data_dir
   - models_dir
   - logs_dir
   - checkpoints_dir
   - vector_store_dir
   - knowledge_graph_dir

============================================================
🎉 Phase 0 Complete - AGI Core Initialized Successfully!
============================================================
```

### 3. Run the tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_config.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

Expected output:
```
tests/unit/test_config.py::TestConfigLoading::test_load_config_success PASSED
tests/unit/test_config.py::TestConfigLoading::test_load_config_file_not_found PASSED
...
tests/unit/test_utils.py::TestYamlFunctions::test_save_yaml_creates_directory PASSED

==================== 35 passed in 0.52s ====================
```

## 🔍 Understanding the Code

### Configuration System

The config system uses YAML for human-readable configuration:

```python
from agi_core import load_config

config = load_config("config.yaml")
print(config["seed"])  # 42
print(config["paths"]["data_dir"])  # data/
```

### Logging System

Structured JSON logging for better observability:

```python
from agi_core import get_logger

logger = get_logger(__name__)
logger.info("Processing started", extra={
    "extra_fields": {"user_id": 123, "action": "train"}
})
```

Output (JSON):
```json
{
  "timestamp": "2026-01-30T14:23:45Z",
  "level": "INFO",
  "name": "my_module",
  "message": "Processing started",
  "user_id": 123,
  "action": "train"
}
```

### Utilities

Common helper functions:

```python
from agi_core import set_seed, ensure_dir, now_str

# Set seed for reproducibility
set_seed(42)

# Create directories
data_dir = ensure_dir("data/experiments")

# Get timestamp
timestamp = now_str("%Y%m%d_%H%M%S")
```

## 📊 Project Structure

```
agi_project/
├── src/
│   └── agi_core/
│       ├── __init__.py          # Package initialization
│       ├── config.py            # ✅ Configuration management
│       ├── logger.py            # ✅ Structured logging
│       ├── utils.py             # ✅ Utility functions
│       └── main.py              # ✅ Entry point
├── tests/
│   └── unit/
│       ├── test_config.py       # ✅ Config tests
│       ├── test_logger.py       # ✅ Logger tests
│       └── test_utils.py        # ✅ Utils tests
├── config.yaml                  # ✅ Configuration file
├── requirements.txt             # ✅ Dependencies
├── README.md                    # ✅ Documentation
├── LICENSE                      # ✅ MIT License
└── .gitignore                   # ✅ Git ignore rules
```

## ✅ Phase 0 Acceptance Criteria

All criteria met! ✅

- [x] Git repo initialized
- [x] Virtual environment can be created
- [x] Configuration loads successfully
- [x] Structured JSON logging works
- [x] Utility functions implemented
- [x] All unit tests pass
- [x] Main script runs without errors
- [x] Project directories created automatically

## 🎯 Next Steps - Phase 1

You're now ready for Phase 1: Core ML Skills & Model Scaffolding

Phase 1 will add:
- Dataset loading (MNIST, Fashion-MNIST)
- Neural network architectures (MLP, CNN)
- Training loop with PyTorch
- Model checkpointing
- Evaluation metrics

When you're ready, just ask: "Let's start Phase 1!"

## 💡 Tips

### Modifying Configuration

Edit `config.yaml` to change settings:

```yaml
# Change device
device: "cpu"  # or "cuda", "mps"

# Change log level
logging:
  level: "DEBUG"  # for more detailed logs

# Adjust random seed
seed: 123  # for different random initialization
```

### Adding Your Own Tests

Create new test files in `tests/unit/`:

```python
# tests/unit/test_my_feature.py
import pytest
from agi_core import my_function

def test_my_feature():
    result = my_function()
    assert result == expected_value
```

### Git Workflow

```bash
# Initialize git (if not done)
git init

# Add Phase 0 files
git add .

# Commit Phase 0
git commit -m "Phase 0: Foundation & environment setup complete"

# Tag the milestone
git tag phase-0
```

## 🐛 Troubleshooting

### Import errors

If you get import errors, make sure you're in the project root:
```bash
cd agi_project
python -m src.agi_core.main
```

### PyTorch not installing

If you don't need GPU support yet:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Tests failing

Make sure you're in the project root and have activated the virtual environment:
```bash
cd agi_project
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m pytest tests/ -v
```

## 📚 Additional Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [pytest Documentation](https://docs.pytest.org/)
- [YAML Syntax](https://yaml.org/spec/1.2/spec.html)
- [Structured Logging](https://www.structlog.org/en/stable/why.html)

---

**Great job completing Phase 0! You've built a solid foundation. Ready for Phase 1? 🚀**

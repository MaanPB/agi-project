"""
Main Entry Point

Demonstrates that Phase 0 is working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import agi_core
sys.path.insert(0, str(Path(__file__).parent.parent))

from agi_core import load_config, get_logger, set_seed, ensure_dir


def main():
    """
    Main entry point for the AGI system.
    """
    print("=" * 60)
    print("AGI Core System - Phase 0 Verification")
    print("=" * 60)
    print()
    
    # Load configuration
    print("📋 Loading configuration...")
    try:
        config = load_config("config.yaml")
        print("✅ Configuration loaded successfully!")
        print(f"   - Seed: {config['seed']}")
        print(f"   - Device: {config['device']}")
        print(f"   - Log level: {config['logging']['level']}")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1
    
    print()
    
    # Set random seed
    print("🎲 Setting random seed...")
    try:
        set_seed(config['seed'])
        print(f"✅ Random seed set to {config['seed']}")
    except Exception as e:
        print(f"❌ Error setting seed: {e}")
        return 1
    
    print()
    
    # Initialize logger
    print("📝 Initializing logger...")
    try:
        logger = get_logger("agi_core.main", level=config['logging']['level'])
        logger.info("AGI core initialized", extra={
            "extra_fields": {
                "seed": config['seed'],
                "device": config['device']
            }
        })
        print("✅ Logger initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing logger: {e}")
        return 1
    
    print()
    
    # Create necessary directories
    print("📁 Creating project directories...")
    try:
        dirs_created = []
        for key, path in config['paths'].items():
            created_path = ensure_dir(path)
            dirs_created.append(key)
        
        print(f"✅ Created {len(dirs_created)} directories:")
        for dir_name in dirs_created:
            print(f"   - {dir_name}")
        
        logger.info("Project directories created", extra={
            "extra_fields": {"directories": dirs_created}
        })
    except Exception as e:
        print(f"❌ Error creating directories: {e}")
        return 1
    
    print()
    print("=" * 60)
    print("🎉 Phase 0 Complete - AGI Core Initialized Successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Run tests: python -m pytest tests/")
    print("  2. Review the code in src/agi_core/")
    print("  3. Ready to proceed to Phase 1!")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

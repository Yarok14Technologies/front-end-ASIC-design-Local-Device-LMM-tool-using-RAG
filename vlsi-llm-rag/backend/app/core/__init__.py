"""
Core module for VLSI Design AI Tool Backend

This module contains core configuration and foundational components:
- Application settings and environment configuration
- Security and authentication utilities
- Database and service configurations
- Core middleware and application setup
"""

from .config import settings, Settings, get_settings

__all__ = [
    "settings",
    "Settings", 
    "get_settings",
]

# Core module metadata
__version__ = "1.0.0"
__author__ = "VLSI Design AI Team"

# Core configuration constants
APP_NAME = "VLSI Design AI Tool"
APP_DESCRIPTION = "Automated Front-End VLSI Design using LLM RAG Pipeline"
APP_VERSION = "1.0.0"

# Available configuration profiles
CONFIG_PROFILES = {
    "development": {
        "debug": True,
        "reload": True,
        "log_level": "DEBUG"
    },
    "production": {
        "debug": False, 
        "reload": False,
        "log_level": "INFO"
    },
    "testing": {
        "debug": True,
        "reload": False,
        "log_level": "WARNING"
    }
}

def get_current_profile() -> str:
    """
    Get the current configuration profile
    
    Returns:
        str: Current profile name (development, production, testing)
    """
    import os
    return os.getenv("APP_ENV", "development")

def is_development() -> bool:
    """
    Check if running in development mode
    
    Returns:
        bool: True if in development mode
    """
    return get_current_profile() == "development"

def is_production() -> bool:
    """
    Check if running in production mode
    
    Returns:
        bool: True if in production mode
    """
    return get_current_profile() == "production"

def is_testing() -> bool:
    """
    Check if running in testing mode
    
    Returns:
        bool: True if in testing mode
    """
    return get_current_profile() == "testing"

# Core application events
APP_EVENTS = {
    "startup": [
        "initialize_services",
        "create_directories", 
        "validate_configuration"
    ],
    "shutdown": [
        "cleanup_resources",
        "close_connections"
    ]
}

print(f"✅ {APP_NAME} Core Module v{__version__} initialized")
print(f"📊 Current profile: {get_current_profile()}")

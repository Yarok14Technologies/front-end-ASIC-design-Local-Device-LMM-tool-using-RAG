"""
Configuration module for VLSI Design AI Tool Backend

This module handles all application configuration including:
- Environment variables and settings
- API configurations
- Service configurations
- Security settings
- File and path configurations
"""

import os
import secrets
from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, validator, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings configuration
    
    All settings can be overridden by environment variables.
    Environment variables should be uppercase with VLSI_ prefix.
    """
    
    # Application Information
    PROJECT_NAME: str = Field(default="VLSI Design AI Tool", env="VLSI_PROJECT_NAME")
    PROJECT_VERSION: str = Field(default="1.0.0", env="VLSI_PROJECT_VERSION")
    PROJECT_DESCRIPTION: str = Field(
        default="Automated Front-End VLSI Design using LLM RAG Pipeline",
        env="VLSI_PROJECT_DESCRIPTION"
    )
    
    # API Configuration
    API_V1_STR: str = Field(default="/api/v1", env="VLSI_API_V1_STR")
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001", 
            "http://127.0.0.1:3001",
        ],
        env="VLSI_BACKEND_CORS_ORIGINS"
    )
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", env="VLSI_HOST")
    PORT: int = Field(default=8000, env="VLSI_PORT")
    RELOAD: bool = Field(default=True, env="VLSI_RELOAD")
    WORKERS: int = Field(default=1, env="VLSI_WORKERS")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="VLSI_ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="VLSI_DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="VLSI_LOG_LEVEL")
    
    # Security
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        env="VLSI_SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="VLSI_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="VLSI_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # LLM Configuration
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    LLM_PROVIDER: str = Field(default="gemini", env="VLSI_LLM_PROVIDER")
    LLM_MODEL: str = Field(default="gemini-pro", env="VLSI_LLM_MODEL")
    LLM_TEMPERATURE: float = Field(default=0.1, env="VLSI_LLM_TEMPERATURE")
    LLM_MAX_TOKENS: int = Field(default=4000, env="VLSI_LLM_MAX_TOKENS")
    LLM_TIMEOUT: int = Field(default=30, env="VLSI_LLM_TIMEOUT")
    
    # RAG Configuration
    CHROMA_DB_PATH: str = Field(default="knowledge_base/vector_db", env="VLSI_CHROMA_DB_PATH")
    EMBEDDING_MODEL: str = Field(default="all-MiniLM-L6-v2", env="VLSI_EMBEDDING_MODEL")
    CHUNK_SIZE: int = Field(default=1000, env="VLSI_CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=200, env="VLSI_CHUNK_OVERLAP")
    SIMILARITY_TOP_K: int = Field(default=3, env="VLSI_SIMILARITY_TOP_K")
    
    # File Upload Configuration
    UPLOAD_DIR: str = Field(default="uploads", env="VLSI_UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=50 * 1024 * 1024, env="VLSI_MAX_FILE_SIZE")  # 50MB
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=[
            '.txt', '.md', '.yaml', '.yml', '.json',
            '.v', '.vh', '.sv', '.vhd', '.vhdl',
            '.pdf', '.doc', '.docx'
        ],
        env="VLSI_ALLOWED_EXTENSIONS"
    )
    
    # RTL Generation Configuration
    DEFAULT_LANGUAGE: str = Field(default="verilog", env="VLSI_DEFAULT_LANGUAGE")
    OPTIMIZATION_TARGET: str = Field(default="balanced", env="VLSI_OPTIMIZATION_TARGET")
    ENABLE_PPA_OPTIMIZATION: bool = Field(default=True, env="VLSI_ENABLE_PPA_OPTIMIZATION")
    MAX_MODULE_COMPLEXITY: int = Field(default=1000, env="VLSI_MAX_MODULE_COMPLEXITY")
    
    # Verification Configuration
    ENABLE_AUTO_VERIFICATION: bool = Field(default=True, env="VLSI_ENABLE_AUTO_VERIFICATION")
    VERIFICATION_TIMEOUT: int = Field(default=60, env="VLSI_VERIFICATION_TIMEOUT")
    MAX_ITERATIONS: int = Field(default=5, env="VLSI_MAX_ITERATIONS")
    
    # Database Configuration (for future use)
    DATABASE_URL: str = Field(default="", env="VLSI_DATABASE_URL")
    
    # Cache Configuration
    REDIS_URL: str = Field(default="", env="VLSI_REDIS_URL")
    CACHE_TTL: int = Field(default=300, env="VLSI_CACHE_TTL")  # 5 minutes
    
    # Monitoring and Logging
    ENABLE_METRICS: bool = Field(default=True, env="VLSI_ENABLE_METRICS")
    LOG_FILE: str = Field(default="logs/app.log", env="VLSI_LOG_FILE")
    ENABLE_ACCESS_LOG: bool = Field(default=True, env="VLSI_ENABLE_ACCESS_LOG")
    
    # Performance Configuration
    MAX_CONCURRENT_GENERATIONS: int = Field(default=3, env="VLSI_MAX_CONCURRENT_GENERATIONS")
    REQUEST_TIMEOUT: int = Field(default=120, env="VLSI_REQUEST_TIMEOUT")
    
    # External Service Configuration
    ENABLE_EXTERNAL_VALIDATION: bool = Field(default=False, env="VLSI_ENABLE_EXTERNAL_VALIDATION")
    EXTERNAL_VALIDATION_URL: str = Field(default="", env="VLSI_EXTERNAL_VALIDATION_URL")
    
    # Feature Flags
    ENABLE_RAG: bool = Field(default=True, env="VLSI_ENABLE_RAG")
    ENABLE_TESTBENCH_GENERATION: bool = Field(default=True, env="VLSI_ENABLE_TESTBENCH_GENERATION")
    ENABLE_PROJECT_MANAGEMENT: bool = Field(default=True, env="VLSI_ENABLE_PROJECT_MANAGEMENT")
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def assemble_allowed_extensions(cls, v):
        """Parse allowed extensions from environment variable"""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v
    
    @validator("GEMINI_API_KEY")
    def validate_gemini_api_key(cls, v):
        """Validate Gemini API key format"""
        if v and len(v) < 20:
            print("⚠️  Warning: Gemini API key seems too short")
        return v
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment value"""
        allowed_environments = ["development", "production", "testing"]
        if v not in allowed_environments:
            raise ValueError(f"Environment must be one of {allowed_environments}")
        return v
    
    @validator("OPTIMIZATION_TARGET")
    def validate_optimization_target(cls, v):
        """Validate optimization target"""
        allowed_targets = ["power", "performance", "area", "balanced"]
        if v not in allowed_targets:
            raise ValueError(f"Optimization target must be one of {allowed_targets}")
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.ENVIRONMENT == "testing"
    
    @property
    def llm_available(self) -> bool:
        """Check if LLM service is available"""
        return bool(self.GEMINI_API_KEY)
    
    @property
    def database_available(self) -> bool:
        """Check if database is configured"""
        return bool(self.DATABASE_URL)
    
    @property
    def cache_available(self) -> bool:
        """Check if cache is configured"""
        return bool(self.REDIS_URL)
    
    def get_feature_status(self) -> Dict[str, bool]:
        """Get status of all feature flags"""
        return {
            "rag_enabled": self.ENABLE_RAG,
            "llm_available": self.llm_available,
            "testbench_generation": self.ENABLE_TESTBENCH_GENERATION,
            "project_management": self.ENABLE_PROJECT_MANAGEMENT,
            "auto_verification": self.ENABLE_AUTO_VERIFICATION,
            "ppa_optimization": self.ENABLE_PPA_OPTIMIZATION,
            "external_validation": self.ENABLE_EXTERNAL_VALIDATION,
            "metrics_enabled": self.ENABLE_METRICS,
            "database_available": self.database_available,
            "cache_available": self.cache_available,
        }
    
    def get_service_config(self) -> Dict[str, Any]:
        """Get service-specific configuration"""
        return {
            "llm": {
                "provider": self.LLM_PROVIDER,
                "model": self.LLM_MODEL,
                "temperature": self.LLM_TEMPERATURE,
                "max_tokens": self.LLM_MAX_TOKENS,
                "timeout": self.LLM_TIMEOUT,
                "available": self.llm_available
            },
            "rag": {
                "db_path": self.CHROMA_DB_PATH,
                "embedding_model": self.EMBEDDING_MODEL,
                "chunk_size": self.CHUNK_SIZE,
                "chunk_overlap": self.CHUNK_OVERLAP,
                "top_k": self.SIMILARITY_TOP_K,
                "enabled": self.ENABLE_RAG
            },
            "file_handling": {
                "upload_dir": self.UPLOAD_DIR,
                "max_file_size": self.MAX_FILE_SIZE,
                "allowed_extensions": self.ALLOWED_EXTENSIONS
            },
            "rtl_generation": {
                "default_language": self.DEFAULT_LANGUAGE,
                "optimization_target": self.OPTIMIZATION_TARGET,
                "enable_ppa": self.ENABLE_PPA_OPTIMIZATION,
                "max_complexity": self.MAX_MODULE_COMPLEXITY
            },
            "verification": {
                "auto_verification": self.ENABLE_AUTO_VERIFICATION,
                "timeout": self.VERIFICATION_TIMEOUT,
                "max_iterations": self.MAX_ITERATIONS
            }
        }
    
    class Config:
        """Pydantic configuration"""
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """
    Get the global settings instance
    
    Returns:
        Settings: Application settings instance
    """
    return settings

def print_config_summary():
    """Print a summary of the current configuration"""
    print("🔧 VLSI Design AI Tool Configuration Summary")
    print(f"   Environment: {settings.ENVIRONMENT}")
    print(f"   Debug Mode: {settings.DEBUG}")
    print(f"   LLM Available: {settings.llm_available}")
    print(f"   RAG Enabled: {settings.ENABLE_RAG}")
    print(f"   Upload Directory: {settings.UPLOAD_DIR}")
    print(f"   Knowledge Base: {settings.CHROMA_DB_PATH}")
    print(f"   API Version: {settings.API_V1_STR}")
    print(f"   Server: {settings.HOST}:{settings.PORT}")

# Print configuration summary when module is imported
if __name__ != "__main__":
    print_config_summary()

# Configuration validation
def validate_configuration() -> Dict[str, Any]:
    """
    Validate the current configuration and return status
    
    Returns:
        Dict with validation results
    """
    validation_results = {
        "overall": "valid",
        "issues": [],
        "warnings": [],
        "recommendations": []
    }
    
    # Check required directories
    required_dirs = [settings.UPLOAD_DIR, settings.CHROMA_DB_PATH]
    for directory in required_dirs:
        if not os.path.exists(directory):
            validation_results["warnings"].append(f"Directory does not exist: {directory}")
    
    # Check LLM configuration
    if not settings.llm_available:
        validation_results["warnings"].append("LLM API key not configured - using fallback mode")
    
    # Check for production configuration issues
    if settings.is_production:
        if settings.DEBUG:
            validation_results["issues"].append("Debug mode should be disabled in production")
        if settings.RELOAD:
            validation_results["issues"].append("Auto-reload should be disabled in production")
        if not settings.SECRET_KEY or settings.SECRET_KEY == secrets.token_urlsafe(32):
            validation_results["issues"].append("Secret key should be set in production")
    
    # Update overall status
    if validation_results["issues"]:
        validation_results["overall"] = "invalid"
    elif validation_results["warnings"]:
        validation_results["overall"] = "warning"
    
    return validation_results

# Environment-specific configuration helpers
def get_development_config() -> Dict[str, Any]:
    """Get development-specific configuration"""
    return {
        "debug": True,
        "reload": True,
        "log_level": "DEBUG",
        "enable_metrics": True,
        "enable_access_log": True
    }

def get_production_config() -> Dict[str, Any]:
    """Get production-specific configuration"""
    return {
        "debug": False,
        "reload": False,
        "log_level": "INFO",
        "enable_metrics": True,
        "enable_access_log": False
    }

def get_testing_config() -> Dict[str, Any]:
    """Get testing-specific configuration"""
    return {
        "debug": True,
        "reload": False,
        "log_level": "WARNING",
        "enable_metrics": False,
        "enable_access_log": False
    }

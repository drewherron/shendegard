"""Configuration management using Pydantic Settings with YAML support."""

import os
import yaml
from typing import Dict, Optional
from pydantic import BaseSettings, validator
from pathlib import Path


class CacheSettings(BaseSettings):
    """Redis cache configuration."""
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    ttl_ip: int = 3600        # 1 hour
    ttl_domain: int = 86400   # 24 hours  
    ttl_hash: int = 604800    # 1 week
    ttl_url: int = 3600       # 1 hour


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""
    requests_per_minute: int = 60
    burst_allowance: int = 10
    enabled: bool = True


class APIKeySettings(BaseSettings):
    """External API credentials."""
    virustotal: Optional[str] = None
    abuseipdb: Optional[str] = None
    otx: Optional[str] = None
    
    class Config:
        env_prefix = "API_KEY_"


class AppSettings(BaseSettings):
    """Main application settings."""
    app_name: str = "Shendegard"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Sub-configurations
    cache: CacheSettings = CacheSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    api_keys: APIKeySettings = APIKeySettings()
    
    @validator('api_keys', pre=True)
    def load_api_keys_from_env(cls, v):
        """Load API keys from environment variables if not provided."""
        if isinstance(v, dict):
            return APIKeySettings(**v)
        return APIKeySettings()
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


def load_config() -> AppSettings:
    """Load configuration from YAML file with environment variable overrides."""
    config_path = Path(__file__).parent / "config.yaml"
    
    # Start with defaults
    config_data = {}
    
    # Load from YAML if it exists
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"Warning: Could not load config.yaml: {e}")
        except Exception as e:
            print(f"Warning: Error reading config file: {e}")
    
    # Create settings (environment variables will override YAML)
    return AppSettings(**config_data)


# Global settings instance
settings = load_config()
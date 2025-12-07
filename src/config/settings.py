"""
Configuration management using Pydantic Settings.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # MinIO Configuration
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket_name: str = "scraped-content"
    minio_secure: bool = False

    # LLM Configuration
    google_api_key: Optional[str] = None
    langextract_model: str = "gemini-2.0-flash-exp"

    # Ollama Configuration (for future use)
    ollama_base_url: Optional[str] = "http://localhost:11434"
    ollama_model: Optional[str] = "gpt-oss:20b"

    # Extraction Settings
    extraction_batch_size: int = 10
    extraction_retry_count: int = 3
    extraction_retry_delay: int = 2  # seconds
    extraction_timeout: int = 30  # seconds
    extraction_max_workers: int = 5  # for parallel processing

    # Rate Limiting
    rate_limit_requests_per_minute: int = 20
    rate_limit_delay_between_requests: int = 3  # seconds

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/extraction.log"


# Global settings instance
settings = Settings()

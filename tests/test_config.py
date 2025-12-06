"""
Test configuration and settings.
"""

import pytest
import os
from unittest.mock import patch
from src.config.settings import settings


class TestSettings:
    """Test settings configuration."""

    def test_default_settings(self):
        """Test default settings values."""
        assert settings.minio_endpoint == "localhost:9000"
        assert settings.minio_secure is False
        assert settings.extraction_max_workers == 5
        assert settings.extraction_retry_count == 3
        assert settings.rate_limit_requests_per_minute == 20

    @patch.dict(
        os.environ,
        {
            "MINIO_ENDPOINT": "test-server:9000",
            "GOOGLE_API_KEY": "test-key",
            "EXTRACTION_MAX_WORKERS": "10",
        },
    )
    def test_environment_override(self):
        """Test environment variable override."""
        # Reload settings with new environment
        from importlib import reload
        from src.config import settings as new_settings

        assert new_settings.settings.minio_endpoint == "test-server:9000"
        assert new_settings.settings.google_api_key == "test-key"
        assert new_settings.settings.extraction_max_workers == 10

    def test_required_fields(self):
        """Test required fields are present."""
        assert hasattr(settings, "minio_endpoint")
        assert hasattr(settings, "minio_access_key")
        assert hasattr(settings, "minio_secret_key")
        assert hasattr(settings, "minio_bucket_name")
        assert hasattr(settings, "google_api_key")
        assert hasattr(settings, "langextract_model")

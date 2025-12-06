"""
Test MinIO manager functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.modules.minio_manager import MinIOManager


class TestMinIOManager:
    """Test MinIO manager operations."""

    @patch("src.modules.minio_manager.Minio")
    @patch("src.modules.minio_manager.settings")
    def test_init(self, mock_settings, mock_minio):
        """Test MinIO manager initialization."""
        mock_settings.minio_endpoint = "test-server:9000"
        mock_settings.minio_access_key = "test-key"
        mock_settings.minio_secret_key = "test-secret"
        mock_settings.minio_secure = False
        mock_settings.minio_bucket_name = "test-bucket"

        manager = MinIOManager()

        assert manager.bucket_name == "test-bucket"
        mock_minio.assert_called_once_with(
            "test-server:9000",
            access_key="test-key",
            secret_key="test-secret",
            secure=False,
        )

    @patch("src.modules.minio_manager.MinIOManager.client")
    def test_list_objects(self, mock_client):
        """Test object listing."""
        # Mock MinIO objects
        mock_obj1 = Mock()
        mock_obj1.object_name = "test1.md"
        mock_obj1.size = 1024
        mock_obj1.last_modified = "2024-01-01"
        mock_obj1.etag = "abc123"

        mock_obj2 = Mock()
        mock_obj2.object_name = "test2.md"
        mock_obj2.size = 2048
        mock_obj2.last_modified = "2024-01-02"
        mock_obj2.etag = "def456"

        mock_client.list_objects.return_value = [mock_obj1, mock_obj2]

        manager = MinIOManager()
        objects = manager.list_objects(prefix="test/", limit=10)

        assert len(objects) == 2
        assert objects[0]["object_name"] == "test1.md"
        assert objects[0]["size"] == 1024
        assert objects[1]["object_name"] == "test2.md"
        assert objects[1]["size"] == 2048

        mock_client.list_objects.assert_called_once_with(
            manager.bucket_name, prefix="test/", recursive=True
        )

    @patch("src.modules.minio_manager.MinIOManager.client")
    def test_list_objects_with_limit(self, mock_client):
        """Test object listing with limit."""
        # Create 10 mock objects
        mock_objects = []
        for i in range(10):
            mock_obj = Mock()
            mock_obj.object_name = f"test{i}.md"
            mock_obj.size = 1024
            mock_obj.last_modified = "2024-01-01"
            mock_obj.etag = f"abc{i}"
            mock_objects.append(mock_obj)

        mock_client.list_objects.return_value = mock_objects

        manager = MinIOManager()
        objects = manager.list_objects(limit=5)

        assert len(objects) == 5
        assert objects[0]["object_name"] == "test0.md"
        assert objects[4]["object_name"] == "test4.md"

    @patch("src.modules.minio_manager.MinIOManager.client")
    def test_download_object(self, mock_client):
        """Test object download."""
        # Mock response
        mock_response = Mock()
        mock_response.read.return_value = b"test content"
        mock_client.get_object.return_value = mock_response

        manager = MinIOManager()
        content = manager.download_object("test.md", as_text=True)

        assert content == "test content"
        mock_client.get_object.assert_called_once_with(manager.bucket_name, "test.md")
        mock_response.read.assert_called_once()
        mock_response.close.assert_called_once()
        mock_response.release_conn.assert_called_once()

    @patch("src.modules.minio_manager.MinIOManager.client")
    def test_upload_json(self, mock_client):
        """Test JSON upload."""
        test_data = {"name": "test", "value": 123}

        manager = MinIOManager()
        result = manager.upload_json("test.json", test_data)

        assert result is True
        mock_client.put_object.assert_called_once()

        # Check call arguments
        call_args = mock_client.put_object.call_args
        assert call_args[0][0] == manager.bucket_name  # bucket name
        assert call_args[0][1] == "test.json"  # object name
        assert call_args[1]["length"] > 0  # content length
        assert "application/json" in call_args[1]["content_type"]

    @patch("src.modules.minio_manager.MinIOManager.client")
    def test_object_exists(self, mock_client):
        """Test object existence check."""
        # Mock stat_object (no exception = exists)
        mock_client.stat_object.return_value = Mock()

        manager = MinIOManager()
        result = manager.object_exists("test.md")

        assert result is True
        mock_client.stat_object.assert_called_once_with(manager.bucket_name, "test.md")

    @patch("src.modules.minio_manager.MinIOManager.client")
    def test_object_not_exists(self, mock_client):
        """Test object not exists."""
        # Mock stat_object (exception = not exists)
        from minio.error import S3Error

        mock_client.stat_object.side_effect = S3Error(
            "Not found", "test", "test", "test", "test", "test"
        )

        manager = MinIOManager()
        result = manager.object_exists("nonexistent.md")

        assert result is False

"""
MinIO client wrapper for object storage operations.
"""

from minio import Minio
from minio.error import S3Error
from typing import List, Dict, Optional
import json
import io
from src.config.settings import settings


class MinIOManager:
    """
    MinIO object storage manager for markdown and JSON file operations.
    """

    def __init__(self):
        """Initialize MinIO client with settings from environment."""
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self.bucket_name = settings.minio_bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"✓ Created bucket: {self.bucket_name}")
            else:
                print(f"✓ Bucket exists: {self.bucket_name}")
        except S3Error as e:
            print(f"✗ Error checking/creating bucket: {e}")
            raise

    def list_objects(
        self, 
        prefix: str = "", 
        recursive: bool = True,
        limit: int = 50
    ) -> List[Dict[str, str]]:
        """
        List objects in bucket with optional prefix filtering.

        Args:
            prefix: Filter objects by prefix (e.g., "scraped-content/")
            recursive: List recursively through subdirectories
            limit: Maximum number of objects to return (None for unlimited)

        Returns:
            List of dictionaries with object metadata
        """
        try:
            objects = self.client.list_objects(
                self.bucket_name, prefix=prefix, recursive=recursive
            )

            result = []
            count = 0
            for obj in objects:
                if limit and count >= limit:
                    break

                result.append(
                    {
                        "object_name": obj.object_name,
                        "size": obj.size,
                        "last_modified": obj.last_modified,
                        "etag": obj.etag,
                    }
                )
                count += 1

            return result
        except S3Error as e:
            print(f"✗ Error listing objects: {e}")
            return []

        def download_object(self, object_name: str, as_text: bool = True) -> Optional[str]:
                """
        Download an object from MinIO.

        Args:
            object_name: Full path to object
            as_text: If True, decode as UTF-8 text

        Returns:
            Object content as string (if as_text=True) or bytes
        """
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()

            if as_text:
                return data.decode("utf-8")
            return data
        except S3Error as e:
            print(f"✗ Error downloading {object_name}: {e}")
            return None

        def upload_json(
        self,
        object_name: str,
        data: dict,
        content_type: str = "application/json; charset=utf-8",
        ) -> bool:
                """
        Upload JSON data to MinIO.

        Args:
            object_name: Full path where to save object
            data: Dictionary to serialize as JSON
            content_type: MIME type

        Returns:
            True if successful, False otherwise
        """
        try:
            json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
            json_stream = io.BytesIO(json_bytes)

            self.client.put_object(
                self.bucket_name,
                object_name,
                json_stream,
                length=len(json_bytes),
                content_type=content_type,
            )

            print(f"✓ Uploaded: {object_name}")
            return True
        except S3Error as e:
            print(f"✗ Error uploading {object_name}: {e}")
            return False

        def put_object(
        self,
        object_name: str,
        data: bytes,
        length: int,
            content_type: str = "application/octet-stream",
            ) -> bool:
                """
        Generic object upload method.

        Args:
            object_name: Full path where to save object
            data: Raw bytes to upload
            length: Length of data
            content_type: MIME type

        Returns:
            True if successful, False otherwise
        """
        try:
            data_stream = io.BytesIO(data)
            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                length=length,
                content_type=content_type,
            )
            print(f"✓ Uploaded: {object_name}")
            return True
        except S3Error as e:
            print(f"✗ Error uploading {object_name}: {e}")
            return False

        def object_exists(self, object_name: str) -> bool:
                """
        Check if an object exists in bucket.

        Args:
            object_name: Full path to object

        Returns:
            True if object exists, False otherwise
        """
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False

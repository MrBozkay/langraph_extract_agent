"""
Test script for MinIO connectivity and basic operations.
"""

import argparse
import os
import sys
import time

# Add project root to Python path for direct execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modules.minio_manager import MinIOManager


def test_minio_connection(prefix="scraped-content/", recursive=False, limit=5):
    """Test MinIO connection and basic operations."""
    print("🧪 Testing MinIO Connection...")
    print(f"📋 Parameters: prefix='{prefix}', recursive={recursive}, limit={limit}")
    print()

    try:
        # Initialize MinIO manager
        minio = MinIOManager()
        print("✅ MinIO client initialized")

        # Test bucket existence
        print(f"✅ Bucket '{minio.bucket_name}' is ready")

        # List objects
        print("\n📁 Listing objects...")
        print("⏱️  Connecting to MinIO...")
        start_time = time.time()

        objects = minio.list_objects(prefix=prefix, recursive=recursive, limit=limit)

        elapsed = time.time() - start_time
        print(f"⚡ Connection established in {elapsed:.2f}s")

        if not objects:
            print("⚠️  No objects found in bucket")
            print("   Upload some markdown files to test extraction")
        else:
            print(f"✅ Found {len(objects)} objects:")
            for obj in objects:
                print(f"   - {obj['object_name']} ({obj['size']} bytes)")

        print("\n✅ All MinIO tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ MinIO test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if MinIO is running: docker-compose ps")
        print("2. Verify .env configuration")
        print("3. Start MinIO: docker-compose up -d minio")
        return False


def main():
    """Main function with command line arguments."""
    parser = argparse.ArgumentParser(description="Test MinIO connectivity")
    parser.add_argument("--prefix", default="scraped-content/", help="Prefix filter")
    parser.add_argument(
        "--recursive", action="store_true", default=False, help="Recursive listing"
    )
    parser.add_argument("--limit", type=int, default=5, help="Limit number of objects")

    args = parser.parse_args()

    success = test_minio_connection(
        prefix=args.prefix, recursive=args.recursive, limit=args.limit
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

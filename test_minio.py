"""
Test script for MinIO connectivity and basic operations.
"""
from src.modules.minio_manager import MinIOManager
import sys


def test_minio_connection():
    """Test MinIO connection and basic operations."""
    print("🧪 Testing MinIO Connection...")
    print()
    
    try:
        # Initialize MinIO manager
        minio = MinIOManager()
        print("✅ MinIO client initialized")
        
        # Test bucket existence
        print(f"✅ Bucket '{minio.bucket_name}' is ready")
        
        # List objects
        print("\n📁 Listing objects...")
        objects = minio.list_objects(prefix="scraped-content/", recursive=True)
        
        if not objects:
            print("⚠️  No objects found in bucket")
            print("   Upload some markdown files to test extraction")
        else:
            print(f"✅ Found {len(objects)} objects:")
            for obj in objects[:5]:  # Show first 5
                print(f"   - {obj['object_name']} ({obj['size']} bytes)")
            if len(objects) > 5:
                print(f"   ... and {len(objects) - 5} more")
        
        print("\n✅ All MinIO tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ MinIO test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if MinIO is running: docker-compose ps")
        print("2. Verify .env configuration")
        print("3. Start MinIO: docker-compose up -d minio")
        return False


if __name__ == "__main__":
    success = test_minio_connection()
    sys.exit(0 if success else 1)

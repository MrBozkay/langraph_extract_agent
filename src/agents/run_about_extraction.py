"""
Simple batch runner for extraction (non-graph approach).

This script iterates through all markdown files in MinIO and extracts
company information, saving results as JSON files.
"""
from src.modules.minio_manager import MinIOManager
from src.agents.about_extractor import AboutExtractor
from src.config.settings import settings


def run_batch_about_extraction():
    """
    Run batch extraction on all markdown files in MinIO.
    """
    print("🚀 Starting batch extraction...")
    print(f"📊 Model: {settings.langextract_model}")
    print(f"🗄️  Bucket: {settings.minio_bucket_name}")
    print()
    
    minio_mgr = MinIOManager()
    extractor = AboutExtractor()

    # List all markdown files
    objects = minio_mgr.list_objects(prefix="scraped-content/", recursive=True)
    md_objects = [obj for obj in objects if obj["object_name"].endswith(".md")]
    
    print(f"📁 Found {len(md_objects)} markdown files")
    print()

    success_count = 0
    skip_count = 0
    error_count = 0

    for idx, obj in enumerate(md_objects, 1):
        object_name = obj["object_name"]
        json_path = object_name.replace(".md", ".about.json")
        
        print(f"[{idx}/{len(md_objects)}] Processing: {object_name}")
        
        # Skip if JSON already exists
        if minio_mgr.object_exists(json_path):
            print(f"⏭️  Skipping (already exists): {json_path}")
            skip_count += 1
            continue

        # Extract company info
        company_info = extractor.extract_from_minio_object(object_name)
        
        if not company_info:
            print(f"⚠️  No data extracted from: {object_name}")
            error_count += 1
            continue

        # Save to MinIO
        data = company_info.model_dump()
        success = minio_mgr.upload_json(json_path, data)
        
        if success:
            success_count += 1
        else:
            error_count += 1
        
        print()

    # Summary
    print("=" * 60)
    print("📊 Extraction Summary:")
    print(f"  ✅ Successful: {success_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📁 Total: {len(md_objects)}")
    print("=" * 60)


if __name__ == "__main__":
    run_batch_about_extraction()

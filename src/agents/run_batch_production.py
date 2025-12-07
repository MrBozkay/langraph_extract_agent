"""
Production-ready batch extraction runner with parallel processing.

Features:
- Parallel processing with thread pool
- Comprehensive error handling
- Statistics tracking
- Progress reporting
- Retry logic
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.agents.about_extractor_v2 import AboutExtractorV2
from src.config.settings import settings
from src.modules.logger import logger
from src.modules.minio_manager import MinIOManager
from src.modules.statistics import ExtractionStatistics


def process_single_file(
    extractor: AboutExtractorV2,
    minio_mgr: MinIOManager,
    object_name: str,
    stats: ExtractionStatistics,
) -> Dict[str, any]:
    """
    Process a single markdown file.

    Args:
        extractor: AboutExtractorV2 instance
        minio_mgr: MinIOManager instance
        object_name: Markdown file path
        stats: Statistics tracker

    Returns:
        Result dictionary
    """
    json_path = object_name.replace(".md", ".about.json")

    try:
        # Skip if JSON already exists
        if minio_mgr.object_exists(json_path):
            logger.info(f"⏭️  Skipping (already exists): {json_path}")
            stats.record_skip()
            return {"status": "skipped", "file": object_name}

        # Extract company info
        start_time = time.time()
        company_info = extractor.extract_from_minio_object(object_name)
        processing_time = time.time() - start_time

        if not company_info:
            logger.warning(f"⚠️  No data extracted from: {object_name}")
            stats.record_error(object_name, "No data extracted")
            return {
                "status": "error",
                "file": object_name,
                "error": "No data extracted",
            }

        # Save to MinIO
        data = company_info.model_dump()
        success = minio_mgr.upload_json(json_path, data)

        if success:
            stats.record_success(processing_time)
            logger.info(f"✅ Successfully processed: {object_name}")
            return {"status": "success", "file": object_name, "time": processing_time}
        else:
            stats.record_error(object_name, "Failed to upload JSON")
            return {"status": "error", "file": object_name, "error": "Upload failed"}

    except Exception as e:
        logger.error(f"❌ Error processing {object_name}: {e}", exc_info=True)
        stats.record_error(object_name, str(e))
        return {"status": "error", "file": object_name, "error": str(e)}


def run_batch_extraction_parallel():
    """
    Run batch extraction with parallel processing.
    """
    logger.info("🚀 Starting production batch extraction...")
    logger.info(f"📊 Model: {settings.langextract_model}")
    logger.info(f"🗄️  MinIO: {settings.minio_endpoint}")
    logger.info(f"📦 Bucket: {settings.minio_bucket_name}")
    logger.info(f"👥 Max Workers: {settings.extraction_max_workers}")
    logger.info(f"🔄 Retry Count: {settings.extraction_retry_count}")
    logger.info(f"⏱️  Rate Limit: {settings.rate_limit_requests_per_minute} req/min")
    print()

    # Initialize components
    minio_mgr = MinIOManager()
    extractor = AboutExtractorV2()
    stats = ExtractionStatistics()

    # List all markdown files
    logger.info("📁 Listing markdown files from MinIO...")
    objects = minio_mgr.list_objects(
        prefix="scraped-content/", recursive=False, limit=50
    )
    md_objects = [
        obj["object_name"] for obj in objects if obj["object_name"].endswith(".md")
    ]

    stats.total_files = len(md_objects)
    logger.info(f"✓ Found {len(md_objects)} markdown files")
    print()

    if not md_objects:
        logger.warning("No markdown files found. Exiting.")
        return

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=settings.extraction_max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_single_file, extractor, minio_mgr, obj, stats): obj
            for obj in md_objects
        }

        # Process completed tasks
        completed = 0
        for future in as_completed(future_to_file):
            completed += 1
            file_name = future_to_file[future]

            try:
                result = future.result()
                progress = f"[{completed}/{len(md_objects)}]"

                if result["status"] == "success":
                    logger.info(f"{progress} ✅ {file_name} ({result['time']:.2f}s)")
                elif result["status"] == "skipped":
                    logger.info(f"{progress} ⏭️  {file_name}")
                else:
                    logger.warning(
                        f"{progress} ❌ {file_name}: {result.get('error', 'Unknown error')}"
                    )

            except Exception as e:
                logger.error(f"[{completed}/{len(md_objects)}] ❌ {file_name}: {e}")
                stats.record_error(file_name, str(e))

    # Print and save statistics
    print()
    stats.print_summary()
    stats.save_to_file()


if __name__ == "__main__":
    run_batch_extraction_parallel()

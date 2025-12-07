"""
Statistics tracking and reporting for extraction pipeline.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class ExtractionStatistics:
    """
    Track and report extraction pipeline statistics.
    """

    def __init__(self):
        """Initialize statistics tracker."""
        self.start_time = time.time()
        self.total_files = 0
        self.successful = 0
        self.skipped = 0
        self.errors = 0
        self.error_details = []
        self.processing_times = []

    def record_success(self, processing_time: float = 0):
        """Record a successful extraction."""
        self.successful += 1
        if processing_time > 0:
            self.processing_times.append(processing_time)

    def record_skip(self):
        """Record a skipped file."""
        self.skipped += 1

    def record_error(self, file_name: str, error: str):
        """Record an error."""
        self.errors += 1
        self.error_details.append(
            {
                "file": file_name,
                "error": str(error),
                "timestamp": datetime.now().isoformat(),
            }
        )

    def get_summary(self) -> Dict[str, Any]:
        """
        Get statistics summary.

        Returns:
            Dictionary with statistics
        """
        elapsed_time = time.time() - self.start_time
        avg_time = (
            sum(self.processing_times) / len(self.processing_times)
            if self.processing_times
            else 0
        )

        return {
            "total_files": self.total_files,
            "successful": self.successful,
            "skipped": self.skipped,
            "errors": self.errors,
            "success_rate": f"{(self.successful / self.total_files * 100) if self.total_files > 0 else 0:.1f}%",
            "elapsed_time": f"{elapsed_time:.2f}s",
            "average_processing_time": f"{avg_time:.2f}s",
            "files_per_second": f"{self.total_files / elapsed_time if elapsed_time > 0 else 0:.2f}",
        }

    def print_summary(self):
        """Print formatted statistics summary."""
        summary = self.get_summary()

        print("\n" + "=" * 70)
        print("📊 EXTRACTION STATISTICS")
        print("=" * 70)
        print(f"  📁 Total Files:          {summary['total_files']}")
        print(f"  ✅ Successful:           {summary['successful']}")
        print(f"  ⏭️  Skipped:              {summary['skipped']}")
        print(f"  ❌ Errors:               {summary['errors']}")
        print(f"  📈 Success Rate:         {summary['success_rate']}")
        print("-" * 70)
        print(f"  ⏱️  Elapsed Time:         {summary['elapsed_time']}")
        print(f"  ⚡ Avg Processing Time:  {summary['average_processing_time']}")
        print(f"  🚀 Files/Second:         {summary['files_per_second']}")
        print("=" * 70)

        if self.error_details:
            print("\n❌ ERROR DETAILS:")
            for idx, error in enumerate(self.error_details[:10], 1):
                print(f"  {idx}. {error['file']}")
                print(f"     Error: {error['error']}")
            if len(self.error_details) > 10:
                print(f"  ... and {len(self.error_details) - 10} more errors")
            print()

    def save_to_file(self, output_path: str = "logs/extraction_stats.json"):
        """
        Save statistics to JSON file.

        Args:
            output_path: Path to save statistics
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        stats = {
            "summary": self.get_summary(),
            "error_details": self.error_details,
            "timestamp": datetime.now().isoformat(),
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        print(f"📊 Statistics saved to: {output_path}")

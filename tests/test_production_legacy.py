"""
Test script for production features (retry, rate limiting, statistics).
"""
from src.modules.retry_handler import retry_with_backoff, RateLimiter
from src.modules.statistics import ExtractionStatistics
from src.modules.logger import logger
import time


@retry_with_backoff(max_retries=3, delay=1)
def test_retry_success():
    """Test successful retry."""
    logger.info("Testing retry with success...")
    return "Success!"


@retry_with_backoff(max_retries=2, delay=1)
def test_retry_failure():
    """Test retry with failure."""
    logger.info("Testing retry with failure...")
    raise ValueError("Simulated error")


def test_rate_limiter():
    """Test rate limiter."""
    logger.info("Testing rate limiter...")
    
    limiter = RateLimiter(requests_per_minute=10, delay_between_requests=1)
    
    for i in range(5):
        limiter.wait_if_needed()
        logger.info(f"Request {i + 1} sent")


def test_statistics():
    """Test statistics tracking."""
    logger.info("Testing statistics...")
    
    stats = ExtractionStatistics()
    stats.total_files = 10
    
    # Simulate processing
    for i in range(10):
        time.sleep(0.1)
        if i < 7:
            stats.record_success(processing_time=0.5 + i * 0.1)
        elif i < 9:
            stats.record_skip()
        else:
            stats.record_error(f"file_{i}.md", "Simulated error")
    
    stats.print_summary()
    stats.save_to_file("logs/test_stats.json")


def main():
    """Run all production feature tests."""
    print("🧪 Testing Production Features\n")
    
    # Test 1: Retry with success
    try:
        result = test_retry_success()
        print(f"✅ Retry test (success): {result}\n")
    except Exception as e:
        print(f"❌ Retry test (success) failed: {e}\n")
    
    # Test 2: Retry with failure
    try:
        test_retry_failure()
        print("❌ Retry test (failure) should have raised exception\n")
    except ValueError as e:
        print(f"✅ Retry test (failure): Correctly raised {e}\n")
    
    # Test 3: Rate limiter
    test_rate_limiter()
    print()
    
    # Test 4: Statistics
    test_statistics()
    print()
    
    print("✅ All production feature tests completed!")


if __name__ == "__main__":
    main()

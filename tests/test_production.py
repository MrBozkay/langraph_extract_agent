"""
Test production features and statistics.
"""

from unittest.mock import patch


from src.modules.retry_handler import RateLimiter
from src.modules.statistics import ExtractionStatistics


class TestExtractionStatistics:
    """Test extraction statistics tracking."""

    def test_init(self):
        """Test statistics initialization."""
        stats = ExtractionStatistics()

        assert stats.total_files == 0
        assert stats.successful == 0
        assert stats.skipped == 0
        assert stats.errors == 0
        assert stats.processing_times == []

    def test_record_success(self):
        """Test success recording."""
        stats = ExtractionStatistics()
        stats.record_success(2.5)

        assert stats.successful == 1
        assert stats.processing_times == [2.5]
        assert stats.total_files == 1

    def test_record_skip(self):
        """Test skip recording."""
        stats = ExtractionStatistics()
        stats.record_skip()

        assert stats.skipped == 1
        assert stats.total_files == 1

    def test_record_error(self):
        """Test error recording."""
        stats = ExtractionStatistics()
        stats.record_error("test.md", "Test error")

        assert stats.errors == 1
        assert stats.total_files == 1
        assert len(stats.error_details) == 1
        assert stats.error_details[0]["file"] == "test.md"
        assert stats.error_details[0]["error"] == "Test error"

    def test_success_rate(self):
        """Test success rate calculation."""
        stats = ExtractionStatistics()

        # No files processed
        assert stats.success_rate() == 0.0

        # Some files processed
        stats.record_success(1.0)
        stats.record_success(2.0)
        stats.record_error("test.md", "error")

        assert stats.success_rate() == 2 / 3  # 2 success out of 3 total

    def test_avg_processing_time(self):
        """Test average processing time calculation."""
        stats = ExtractionStatistics()

        # No processing times
        assert stats.avg_processing_time() == 0.0

        # Some processing times
        stats.record_success(1.0)
        stats.record_success(3.0)
        stats.record_success(2.0)

        assert stats.avg_processing_time() == 2.0  # (1+3+2)/3

    def test_files_per_second(self):
        """Test files per second calculation."""
        stats = ExtractionStatistics()

        # Mock elapsed time
        with patch("time.time") as mock_time:
            mock_time.side_effect = [0, 10]  # 10 seconds elapsed
            stats.start_time = 0

            stats.record_success(1.0)
            stats.record_success(2.0)
            stats.record_success(3.0)

            assert stats.files_per_second() == 3 / 10  # 3 files in 10 seconds


class TestRateLimiter:
    """Test rate limiting functionality."""

    def test_init(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(requests_per_minute=10, delay_between_requests=6)

        assert limiter.requests_per_minute == 10
        assert limiter.delay_between_requests == 6
        assert limiter.request_times == []

    @patch("time.time")
    def test_can_proceed_true(self, mock_time):
        """Test rate limiter allows request."""
        mock_time.return_value = 1000.0

        limiter = RateLimiter(requests_per_minute=10, delay_between_requests=6)

        # First request should always be allowed
        assert limiter.can_proceed() is True

    @patch("time.time")
    def test_can_proceed_rate_limit(self, mock_time):
        """Test rate limiter blocks when rate limit exceeded."""
        # Simulate 10 requests within 1 minute
        base_time = 1000.0
        mock_time.side_effect = [base_time + i for i in range(15)]

        limiter = RateLimiter(requests_per_minute=10, delay_between_requests=0)

        # First 10 requests should be allowed
        for i in range(10):
            assert limiter.can_proceed() is True
            limiter.record_request()

        # 11th request should be blocked
        assert limiter.can_proceed() is False

    @patch("time.time")
    def test_can_proceed_delay(self, mock_time):
        """Test rate limiter blocks when delay not passed."""
        # Simulate requests with insufficient delay
        base_time = 1000.0
        mock_time.side_effect = [base_time, base_time + 2]  # Only 2 seconds passed

        limiter = RateLimiter(requests_per_minute=10, delay_between_requests=6)

        # First request
        assert limiter.can_proceed() is True
        limiter.record_request()

        # Second request should be blocked (need 6 seconds, only 2 passed)
        assert limiter.can_proceed() is False

    def test_record_request(self):
        """Test request recording."""
        limiter = RateLimiter(requests_per_minute=10, delay_between_requests=6)

        assert len(limiter.request_times) == 0

        limiter.record_request()

        assert len(limiter.request_times) == 1
        assert limiter.request_times[0] > 0

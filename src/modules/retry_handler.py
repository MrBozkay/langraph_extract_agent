"""
Retry logic and error handling utilities.
"""

import functools
import time
from typing import Any, Callable, Optional

from src.config.settings import settings
from src.modules.logger import logger


def retry_with_backoff(
    max_retries: Optional[int] = None,
    delay: Optional[int] = None,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default from settings)
        delay: Initial delay in seconds (default from settings)
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry

    Returns:
        Decorated function with retry logic
    """
    if max_retries is None:
        max_retries = settings.extraction_retry_count
    if delay is None:
        delay = settings.extraction_retry_delay

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {e}"
                        )
                        logger.info(f"Retrying in {current_delay} seconds...")
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {e}"
                        )

            raise last_exception

        return wrapper

    return decorator


class RateLimiter:
    """
    Simple rate limiter to control request frequency.
    """

    def __init__(
        self,
        requests_per_minute: Optional[int] = None,
        delay_between_requests: Optional[int] = None,
    ):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute
            delay_between_requests: Minimum delay between requests in seconds
        """
        self.requests_per_minute = (
            requests_per_minute or settings.rate_limit_requests_per_minute
        )
        self.delay_between_requests = (
            delay_between_requests or settings.rate_limit_delay_between_requests
        )
        self.last_request_time = 0
        self.request_count = 0
        self.minute_start = time.time()

    def wait_if_needed(self):
        """
        Wait if rate limit is reached.
        """
        current_time = time.time()

        # Reset counter every minute
        if current_time - self.minute_start >= 60:
            self.request_count = 0
            self.minute_start = current_time

        # Check requests per minute limit
        if self.request_count >= self.requests_per_minute:
            sleep_time = 60 - (current_time - self.minute_start)
            if sleep_time > 0:
                logger.info(f"Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                self.request_count = 0
                self.minute_start = time.time()

        # Check delay between requests
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.delay_between_requests:
            sleep_time = self.delay_between_requests - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1


# Global rate limiter instance
rate_limiter = RateLimiter()

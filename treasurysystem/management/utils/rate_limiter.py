import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, calls_per_minute=30):
        self.calls_per_minute = calls_per_minute
        self.interval = 60.0 / calls_per_minute
        self.last_call = 0
        
    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()

def rate_limited(calls_per_minute=30, max_retries=3):
    limiter = RateLimiter(calls_per_minute)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    limiter.wait()
                    return func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e) and retries < max_retries:
                        wait_time = 2 ** retries  # Exponential backoff
                        logger.warning(f"Rate limit hit, waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        retries += 1
                    else:
                        raise
            return None
        return wrapper
    return decorator

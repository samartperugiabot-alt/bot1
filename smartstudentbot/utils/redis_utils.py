import aioredis
from aioredis import Redis
import json
from typing import Optional, Any
import asyncio

from ..config import REDIS_URL
from .logger import logger

class RedisManager:
    """
    A Redis manager that handles connections and provides utility functions.
    Includes a fallback to an in-memory dictionary if Redis is unavailable.
    """
    def __init__(self, redis_url: Optional[str]):
        self.redis_url = redis_url
        self.redis: Optional[Redis] = None
        self._fallback_cache = {}
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initializes the Redis connection pool."""
        if self.redis_url:
            try:
                self.redis = aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
                await self.redis.ping()
                logger.info("Successfully connected to Redis.")
            except (aioredis.exceptions.ConnectionError, aioredis.exceptions.TimeoutError) as e:
                logger.error(f"Could not connect to Redis: {e}. Using in-memory fallback cache.")
                self.redis = None
        else:
            logger.warning("REDIS_URL not provided. Using in-memory fallback cache.")
            self.redis = None

    async def close(self):
        """Closes the Redis connection."""
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed.")

    async def set_json(self, key: str, data: Any, ttl: int):
        """Sets a JSON value in Redis with a TTL."""
        if self.redis:
            await self.redis.setex(key, ttl, json.dumps(data))
        else:
            async with self._lock:
                # Fallback doesn't support TTL, but we store it anyway
                self._fallback_cache[key] = (json.dumps(data), asyncio.get_event_loop().time() + ttl)

    async def get_json(self, key: str) -> Optional[Any]:
        """Gets a JSON value from Redis."""
        if self.redis:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        else:
            async with self._lock:
                if key in self._fallback_cache:
                    data, expiry = self._fallback_cache[key]
                    # Simple expiry check for fallback
                    if asyncio.get_event_loop().time() < expiry:
                        return json.loads(data)
                    else:
                        del self._fallback_cache[key]
                return None

    async def get_user_lang(self, user_id: int) -> Optional[str]:
        """Gets user language from cache."""
        key = f"user:{user_id}:lang"
        if self.redis:
            return await self.redis.get(key)
        else:
            # In fallback, this would likely be part of a larger user profile object
            user_profile = await self.get_json(f"user:{user_id}:profile")
            return user_profile.get("lang") if user_profile else None

    async def set_user_lang(self, user_id: int, lang: str):
        """Sets user language in cache."""
        key = f"user:{user_id}:lang"
        if self.redis:
            await self.redis.set(key, lang)
        else:
            # In fallback, update the profile object
            profile_key = f"user:{user_id}:profile"
            profile = await self.get_json(profile_key) or {}
            profile['lang'] = lang
            await self.set_json(profile_key, profile, ttl=3600) # 1 hour TTL for example

    async def check_rate_limit(self, key: str, limit: int, period: int) -> bool:
        """
        Checks if a user has exceeded a rate limit.
        Returns True if the request is allowed, False otherwise.
        """
        if not self.redis:
            # Rate limiting is disabled in fallback mode to avoid complexity
            return True

        # This is a simple but effective rate limiting algorithm using a sliding window.
        # It's memory-efficient as it only stores timestamps for the current window.
        now = asyncio.get_event_loop().time()
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - period) # Remove old timestamps
        pipe.zadd(key, {str(now): now}) # Add current request timestamp
        pipe.zcard(key) # Count requests in the window
        pipe.expire(key, period) # Ensure the key expires eventually
        results = await pipe.execute()

        count = results[2]
        return count <= limit


# Global instance
redis_manager = RedisManager(REDIS_URL)

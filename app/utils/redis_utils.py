import redis
from typing import Optional, List


class RedisUtils:
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get(self, key: str) -> Optional[str]:
        """Retrieve the value associated with a key."""
        return self.client.get(key)

    def set(self, key: str, value: str, expire: Optional[int] = None) -> bool:
        """Set the value for a key with an optional expiration time."""
        return self.client.set(key, value, ex=expire)

    def incr(self, key: str, amount: int = 1) -> int:
        """Increment the integer value of a key by a given amount."""
        return self.client.incr(key, amount)

    def decr(self, key: str, amount: int = 1) -> int:
        """Decrement the integer value of a key by a given amount."""
        return self.client.decr(key, amount)

    def zadd(self, key: str, mapping: dict) -> int:
        """Add members with scores to a sorted set."""
        return self.client.zadd(key, mapping)

    def zrangebyscore(self, key: str, min_score: float, max_score: float) -> List[str]:
        """Retrieve members of a sorted set within a given score range."""
        return self.client.zrangebyscore(key, min_score, max_score)

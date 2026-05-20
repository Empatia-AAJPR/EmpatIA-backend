from typing import Any

from redis import Redis, RedisError

from core.redis.exceptions import RedisReadException, RedisWriterException
from core.redis.interfaces import IRedisRepository


class RedisRepository(IRedisRepository):
    def __init__(self, conn: Redis) -> None:
        self.__conn = conn

    def h_insert(self, key: str, field: str, value: Any):
        try:
            self.__conn.hset(key, field, value)
        
        except RedisError as e:
            raise RedisWriterException(f'error to send hash redis')
        
    def h_get(self, key: str, field: str):
        try:
            return self.__conn.hget(key, field)

        except RedisError as e:
            raise RedisReadException(f'error from get hash redis')
        
    def h_insert_ex(self, key: str, field: str, value: Any, ex: int):
        try:
            self.__conn.hset(key, field, value)
            self.__conn.expire(key, ex)
        
        except RedisError as e:
            raise RedisWriterException(f'error to send hash redis with expire')

    def h_get_all(self, key: str):
        try:
            return self.__conn.hgetall(key)

        except RedisError as e:
            raise RedisReadException(f'error from get all hash redis')
    
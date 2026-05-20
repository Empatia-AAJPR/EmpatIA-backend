from redis import Redis

from dotenv import load_dotenv

import os

load_dotenv()


class RedisConnectionHandler:
    def __init__(self) -> None:
        self.__host = os.getenv('R_HOST', '')
        self.__port = int(os.getenv('R_PORT', ''))
        self.__responses = bool(os.getenv('R_RESPONSES', True))
        self.__username = os.getenv('R_USERNAME', '')
        self.__password = os.getenv("R_PASSWORD", '')

    def connect(self) -> Redis:
        self.__conn = Redis(
            host=self.__host,
            port=self.__port,
            decode_responses=self.__responses,
            username=self.__username,
            password=self.__password
        )
        return self.__conn

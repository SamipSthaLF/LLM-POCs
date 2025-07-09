from typing import Optional
from dataclasses import dataclass
import redis


@dataclass
class Config:
    openai_api_key: str
    redis_host: str
    redis_port: int
    redis_db: Optional[int]
    redis_password: str

    @staticmethod
    def load(
        openai_api_key: str,
        redis_host: str,
        redis_port: int,
        redis_db: Optional[int],
        redis_password: str,
    ) -> "Config":
        """
        Load configuration from provided arguments.
        """
        config = Config(
            openai_api_key=openai_api_key,
            redis_host=redis_host,
            redis_port=redis_port,
            redis_db=redis_db,
            redis_password=redis_password,
        )

        # Attempt Redis connection to validate config
        try:
            r = None
            if redis_db is not None:
                r = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    password=redis_password,
                )
            else:
                r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)
            r.ping()
            print("[config] Redis connection successful.")
        except Exception as e:
            print(f"[config] Redis connection failed: {e}")

        return config

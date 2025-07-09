import redis
import numpy as np
import hashlib
import json
from typing import List


class UserVectorStore:
    def __init__(self, redis_url: str = None, host: str = "localhost", port: int = 6379, db: int = None, password: str = "", namespace: str = "style_mail_vector"):
        kwargs = {"host": host, "port": port, "password": password}
        if db is not None:
            kwargs["db"] = db
        self.redis = redis.Redis(**kwargs)
        self.namespace = namespace

    def _user_key(self, user_id: str) -> str:
        prefix = f"{self.namespace}:" if self.namespace else ""
        return f"{prefix}user:{user_id}:vectors"

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def store_embedding(self, user_id: str, text: str, embedding: List[float]) -> None:
        key = self._user_key(user_id)
        doc_id = self._hash_text(text)
        self.redis.hset(key, doc_id, json.dumps({"text": text, "embedding": embedding}))

    def get_all_embeddings(self, user_id: str) -> List[dict]:
        key = self._user_key(user_id)
        try:
            raw = self.redis.hgetall(key)
            return [json.loads(v) for v in raw.values()]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve embeddings from Redis for user '{user_id}': {e}")

    def clear_user_data(self, user_id: str) -> None:
        self.redis.delete(self._user_key(user_id))

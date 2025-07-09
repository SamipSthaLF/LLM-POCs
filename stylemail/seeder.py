from openai import OpenAI
from typing import List
from stylemail.vectorstore import UserVectorStore


class StyleSeeder:
    def __init__(self, openai_api_key: str, vector_store: UserVectorStore):
        self.client = OpenAI(api_key=openai_api_key)
        self.vector_store = vector_store

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embeddings.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            return [d.embedding for d in response.data]
        except Exception as e:
            raise RuntimeError(f"Failed to embed texts with OpenAI API: {e}")

    def seed_user_style(self, user_id: str, samples: List[str]) -> None:
        """
        Embed and store a user's writing samples in the Redis vector store.
        """
        embeddings = self.embed_texts(samples)
        for text, emb in zip(samples, embeddings):
            self.vector_store.store_embedding(user_id, text, emb)

import os
import pytest
from stylemail.api import seed_user_style, generate_email
from stylemail.config import Config


@pytest.fixture
def config():
    return Config.load(
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
        openai_api_key=os.getenv("OPENAI_API_KEY", "sk-test")
    )


def test_seed_and_generate(monkeypatch, config):
    """Test happy path for seeding and generating an email."""
    user_id = "test_user"
    samples = ["Hi there!", "Thanks for your message."]
    prompt = "Follow up on the proposal"

    # Mock OpenAI embedding and chat
    monkeypatch.setattr("openai.Embedding.create", lambda **kwargs: {
        "data": [{"embedding": [0.1] * 1536} for _ in kwargs["input"]]
    })
    monkeypatch.setattr("openai.ChatCompletion.create", lambda **kwargs: {
        "choices": [{"message": {"content": "This is a test email."}}]
    })

    # Mock Redis vector store methods
    monkeypatch.setattr("stylemail.vectorstore.UserVectorStore.store_embedding", lambda self, uid, text, emb: None)
    monkeypatch.setattr("stylemail.vectorstore.UserVectorStore.get_all_embeddings", lambda self, uid: [
        {"text": s, "embedding": [0.1] * 1536} for s in samples
    ])

    seed_user_style(user_id, samples, config=config)
    result = generate_email(user_id, prompt, config=config)

    assert "body" in result
    assert "test email" in result["body"].lower()


def test_invalid_inputs():
    with pytest.raises(ValueError):
        seed_user_style("", ["sample"])
    with pytest.raises(ValueError):
        seed_user_style("user", [])
    with pytest.raises(ValueError):
        generate_email("", "prompt")
    with pytest.raises(ValueError):
        generate_email("user", "")


def test_missing_style(monkeypatch, config):
    monkeypatch.setattr("openai.Embedding.create", lambda **kwargs: {
        "data": [{"embedding": [0.1] * 1536}]
    })
    monkeypatch.setattr("stylemail.vectorstore.UserVectorStore.get_all_embeddings", lambda self, uid: [])

    with pytest.raises(RuntimeError, match="No style data found"):
        generate_email("user123", "prompt", config=config)

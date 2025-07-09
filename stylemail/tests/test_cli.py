import subprocess
import sys
import os
import pytest


import shutil

@pytest.mark.skipif(
    shutil.which("python3") is None or not os.getenv("OPENAI_API_KEY"),
    reason="Requires real OpenAI key and python3 in PATH"
)
def test_cli_seed_and_generate(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")

    # Mock OpenAI
    monkeypatch.setattr("openai.Embedding.create", lambda **kwargs: {
        "data": [{"embedding": [0.1] * 1536} for _ in kwargs["input"]]
    })
    monkeypatch.setattr("openai.ChatCompletion.create", lambda **kwargs: {
        "choices": [{"message": {"content": "CLI test email."}}]
    })

    # Mock Redis
    monkeypatch.setattr("stylemail.vectorstore.UserVectorStore.store_embedding", lambda self, uid, text, emb: None)
    monkeypatch.setattr("stylemail.vectorstore.UserVectorStore.get_all_embeddings", lambda self, uid: [
        {"text": "Thanks!", "embedding": [0.1] * 1536}
    ])

    result = subprocess.run(
        [sys.executable, "-m", "stylemail.cli", "generate", "cli_user", "Follow up"],
        capture_output=True,
        text=True,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    )

    assert "Generated Email" in result.stdout
    assert "CLI test email" in result.stdout

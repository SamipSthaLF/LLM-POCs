import logging
from typing import List, Dict, Any
from stylemail.config import Config
from stylemail.vectorstore import UserVectorStore
from stylemail.seeder import StyleSeeder
from stylemail.generator import EmailGenerator, NudgeSummaryGenerator, NudgeEmailGenerator


def seed_user_style(user_id: str, samples: List[str], store: UserVectorStore, openai_api_key: str) -> None:
    """
    Store a user's writing style by embedding sample texts and saving them to Redis.
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non-empty string")
    if not samples or not all(isinstance(s, str) for s in samples):
        raise ValueError("samples must be a list of non-empty strings")

    seeder = StyleSeeder(openai_api_key, store)
    logging.info(f"Seeding style for user '{user_id}' with {len(samples)} samples.")
    seeder.seed_user_style(user_id, samples)


def generate_email(user_id: str, subject: str, prompt: str, store: UserVectorStore, openai_api_key: str) -> Dict[str, str]:
    """
    Generate a personalized email using the user's writing style and a given prompt.
    Returns a dictionary with 'subject' and 'body'.
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non-empty string")
    if not subject or not isinstance(subject, str):
        raise ValueError("subject must be a non-empty string")
    if not prompt or not isinstance(prompt, str):
        raise ValueError("prompt must be a non-empty string")

    generator = EmailGenerator(openai_api_key, store)
    logging.info(f"[generate_email] user='{user_id}' subject='{subject}' prompt='{prompt}'")
    return generator.generate_email(user_id, subject, prompt)
def generate_nudge_email(user_id: str, prompt: str, nudges: List[Dict[str, str]], store: UserVectorStore, openai_api_key: str) -> Dict[str, str]:
    """
    Generate an email for a list of nudges based on a given prompt.
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non-empty string")
    if not prompt or not isinstance(prompt, str):
        raise ValueError("prompt must be a non-empty string")
    if not nudges or not all(isinstance(n, dict) for n in nudges):
        raise ValueError("nudges must be a list of dictionaries with 'title', 'instructions', and 'metrics' keys")

    generator = NudgeEmailGenerator(openai_api_key, store)
    logging.info(f"[generate_nudge_email] user='{user_id}' prompt='{prompt}' nudges='{nudges}'")
    return generator.generate_email(user_id, prompt, nudges)
def generate_nudge_summary(user_id: str, prompt: str, nudges: List[Dict[str, str]], store: UserVectorStore, openai_api_key: str) -> Dict[str, str]:
    """
    Generate a summary for a list of nudges based on a given prompt.
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("user_id must be a non-empty string")
    if not prompt or not isinstance(prompt, str):
        raise ValueError("prompt must be a non-empty string")
    if not nudges or not all(isinstance(n, dict) for n in nudges):
        raise ValueError("nudges must be a list of dictionaries with 'title', 'instructions', and 'metrics' keys")

    generator = NudgeSummaryGenerator(openai_api_key, store)
    logging.info(f"[generate_nudge_summary] user='{user_id}' prompt='{prompt}' nudges='{nudges}'")
    return generator.generate_summary(user_id, prompt, nudges)

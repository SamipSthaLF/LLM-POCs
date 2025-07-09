import sys
import os
from .api import seed_user_style, generate_email, generate_nudge_email, generate_nudge_summary
from .vectorstore import UserVectorStore


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python cli.py seed <user_id> <sample1> [<sample2> ...]")
        print("  python cli.py generate <user_id> <subject> <prompt>")
        sys.exit(1)

    command = sys.argv[1]
    user_id = sys.argv[2]

    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_password = os.getenv("REDIS_PASSWORD", "")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")

    auth_part = f":{redis_password}@" if redis_password else ""
    redis_url = f"redis://{auth_part}{redis_host}:{redis_port}/{redis_db}"

    store = UserVectorStore(
        redis_url=redis_url,
        host=redis_host,
        port=redis_port,
        db=redis_db,
        password=redis_password,
    )

    if command == "seed":
        samples = sys.argv[3:]
        if not samples:
            print("Please provide at least one writing sample.")
            sys.exit(1)
        seed_user_style(user_id, samples, store=store, openai_api_key=openai_api_key)
        print(f"Seeded style for user '{user_id}' with {len(samples)} samples.")
    elif command == "generate":
        if len(sys.argv) < 5:
            print("Please provide a subject and a prompt.")
            sys.exit(1)
        subject = sys.argv[3]
        prompt = " ".join(sys.argv[4:])
        result = generate_email(user_id, subject, prompt, store=store, openai_api_key=openai_api_key)
        print("Generated Email:")
        print("Subject:", result["subject"])
        print("Body:\n", result["body"])
    elif command == "nudge":
        if len(sys.argv) < 4:
            print("Please provide a prompt and a list of nudges.")
            sys.exit(1)
        prompt = sys.argv[3]
        nudges = sys.argv[4:]
        if command == "nudge":
            result = generate_nudge_summary(user_id, prompt, nudges, store=store, openai_api_key=openai_api_key)
            print("Generated Nudge Summary:")
            print("Summary:\n", result["summary"])
        elif command == "nudge-email":
            result = generate_nudge_email(user_id, prompt, nudges, store=store, openai_api_key=openai_api_key)
            print("Generated Nudge Email:")
            print("Subject:", result["subject"])
            print("Body:\n", result["body"])
            store.clear_user_data(user_id)
            print(f"Cleared all cached embeddings for user '{user_id}'.")
    elif command == "nudge-email":
        if len(sys.argv) < 4:
            print("Please provide a prompt and a list of nudges.")
            sys.exit(1)
        prompt = sys.argv[3]
        nudges = sys.argv[4:]
        result = generate_nudge_email(user_id, prompt, nudges, store=store, openai_api_key=openai_api_key)
        print("Generated Nudge Email:")
        print("Subject:", result["subject"])
        print("Body:\n", result["body"])
        store.clear_user_data(user_id)
        print(f"Cleared all cached embeddings for user '{user_id}'.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

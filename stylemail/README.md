# StyleMail

A pluggable Python module for generating personalized, style-aware emails using OpenAI and Redis.

## Features

- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Multi-user style memory via Redis
- ✅ Stateless, embeddable design
- ✅ CLI and Node.js wrapper
- ✅ Configurable via env or args

## Installation

```bash
pip install -r requirements.txt
```

## Usage (Python)

```python
from stylemail import seed_user_style, generate_email

seed_user_style("user123", ["Thanks for your message.", "Looking forward to our meeting."])
email = generate_email("user123", "Follow up on the proposal")
print(email["body"])
```

## CLI

```bash
python -m stylemail.cli seed user123 "Sample 1" "Sample 2"
python -m stylemail.cli generate user123 "Follow up on the proposal"
```

## Node.js

```js
const { seedUserStyle, generateEmail } = require("./js/stylemail");

seedUserStyle("user123", ["Thanks!", "See you soon."], console.log);
generateEmail("user123", "Follow up on the proposal", console.log);
```

## Configuration

Set via environment variables:

- `OPENAI_API_KEY`
- `REDIS_URL` (default: `redis://localhost:6379`)

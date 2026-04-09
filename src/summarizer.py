"""
summarizer.py - Uses OpenAI LLM to generate readable summaries for raw technical logs.
"""

import yaml
from openai import OpenAI


def _get_client() -> OpenAI:
    """Load the OpenAI API key from config and return a client."""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return OpenAI(api_key=config["openai_api_key"])


def summarize_alert(log: str) -> str:
    """
    Uses OpenAI's chat completion to generate a human-readable summary
    of a raw security log entry.

    Args:
        log: A single raw log entry string.

    Returns:
        A concise summary of the log.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Security Operations Center (SOC) analyst assistant. "
                    "Summarize the following security log entry into a clear, concise, "
                    "human-readable alert summary. Focus on what happened, the source, "
                    "the target, and the potential impact. Keep it to 1-2 sentences."
                ),
            },
            {"role": "user", "content": log},
        ],
        temperature=0.3,
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()

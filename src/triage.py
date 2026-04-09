"""
triage.py - Severity classification of security log entries using OpenAI.
"""

import yaml
from openai import OpenAI


def _get_client() -> OpenAI:
    """Load the OpenAI API key from config and return a client."""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return OpenAI(api_key=config["openai_api_key"])


def triage_alert(log: str) -> str:
    """
    Classifies the severity of a security log entry.

    Args:
        log: A single raw log entry string.

    Returns:
        A severity level string: Critical, High, Medium, Low, or Informational.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Security Operations Center (SOC) triage analyst. "
                    "Classify the severity of the following security log entry. "
                    "Respond with ONLY one of these severity levels: "
                    "Critical, High, Medium, Low, or Informational. "
                    "Base your classification on the potential impact, "
                    "the type of activity, and common threat intelligence."
                ),
            },
            {"role": "user", "content": log},
        ],
        temperature=0.1,
        max_tokens=20,
    )

    return response.choices[0].message.content.strip()

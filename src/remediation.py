"""
remediation.py - Suggests first response actions for security alerts using OpenAI.
"""

import yaml
from openai import OpenAI


def _get_client() -> OpenAI:
    """Load the OpenAI API key from config and return a client."""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return OpenAI(api_key=config["openai_api_key"])


def suggest_remediation(log: str) -> str:
    """
    Uses OpenAI to suggest first response / remediation actions
    for a given security log entry.

    Args:
        log: A single raw log entry string.

    Returns:
        A string with recommended remediation steps.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Security Operations Center (SOC) remediation advisor. "
                    "Based on the following security log entry, suggest concrete first "
                    "response actions the SOC team should take. Examples include: "
                    "blocking an IP, isolating a host, disabling a user account, "
                    "escalating to incident response, collecting forensic artifacts, etc. "
                    "Keep your response to 1-3 actionable bullet points."
                ),
            },
            {"role": "user", "content": log},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()

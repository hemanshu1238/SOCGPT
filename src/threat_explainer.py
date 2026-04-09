"""
threat_explainer.py - Q&A with LLM for analyst follow-up questions about threats.
"""

import yaml
from openai import OpenAI


def _get_client() -> OpenAI:
    """Load the OpenAI API key from config and return a client."""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return OpenAI(api_key=config["openai_api_key"])


def explain_threat(log: str, question: str) -> str:
    """
    Allows an analyst to ask follow-up questions about a specific
    security log entry or threat.

    Args:
        log: The raw log entry providing context.
        question: The analyst's follow-up question.

    Returns:
        A detailed explanation from the LLM.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior Security Operations Center (SOC) analyst assistant. "
                    "An analyst is reviewing a security log and has a follow-up question. "
                    "Provide a clear, detailed, and actionable explanation. "
                    "Reference specific indicators from the log when relevant."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Security Log Entry:\n{log}\n\n"
                    f"Analyst Question:\n{question}"
                ),
            },
        ],
        temperature=0.4,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()

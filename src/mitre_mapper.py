"""
mitre_mapper.py - Maps detected behavior to MITRE ATT&CK techniques.
Uses rule-based pattern matching first, with an LLM fallback for unknown patterns.
"""

import re

import yaml
from openai import OpenAI

# Rule-based mappings for common log patterns
MITRE_RULES = {
    r"powershell": "T1059 – Command and Scripting Interpreter",
    r"cmd\.exe": "T1059 – Command and Scripting Interpreter",
    r"login fail|failed login|authentication fail": "T1110 – Brute Force",
    r"ssh.*fail": "T1110 – Brute Force",
    r"privilege escalation|sudo|runas": "T1078 – Valid Accounts",
    r"lateral movement|psexec|wmic": "T1021 – Remote Services",
    r"exfiltrat|data transfer|upload.*external": "T1041 – Exfiltration Over C2 Channel",
    r"phishing|spear.?phish": "T1566 – Phishing",
    r"malware|trojan|ransomware": "T1204 – User Execution",
    r"registry|reg\.exe": "T1112 – Modify Registry",
    r"scheduled task|cron|at\.exe": "T1053 – Scheduled Task/Job",
    r"dns.*tunnel|dns.*exfil": "T1071 – Application Layer Protocol",
    r"keylog": "T1056 – Input Capture",
    r"credential.*dump|mimikatz|lsass": "T1003 – OS Credential Dumping",
}


def _get_client() -> OpenAI:
    """Load the OpenAI API key from config and return a client."""
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return OpenAI(api_key=config["openai_api_key"])


def mitre_mapping(log: str) -> str:
    """
    Maps a security log entry to a MITRE ATT&CK technique.

    First attempts rule-based matching against known patterns.
    Falls back to OpenAI for unknown log types.

    Args:
        log: A single raw log entry string.

    Returns:
        A MITRE ATT&CK technique ID and name string.
    """
    # Try rule-based matching first
    log_lower = log.lower()
    for pattern, technique in MITRE_RULES.items():
        if re.search(pattern, log_lower):
            return technique

    # Fallback to LLM for unknown patterns
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a MITRE ATT&CK framework expert. "
                        "Map the following security log entry to the most relevant "
                        "MITRE ATT&CK technique. Respond with ONLY the technique ID "
                        "and name in the format: TXXXX – Technique Name. "
                        "If no technique matches, respond with: Unknown Technique."
                    ),
                },
                {"role": "user", "content": log},
            ],
            temperature=0.1,
            max_tokens=60,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Unknown Technique"

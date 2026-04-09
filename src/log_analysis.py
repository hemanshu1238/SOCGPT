"""
log_analysis.py - Handles log ingestion from files.
"""


def load_logs(log_path: str) -> list[str]:
    """
    Reads a log file and returns a list of non-empty log lines.

    Args:
        log_path: Path to the log file.

    Returns:
        A list of log entry strings.
    """
    with open(log_path, "r", encoding="utf-8") as f:
        logs = [line.strip() for line in f if line.strip()]
    return logs

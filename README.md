# SOCGPT 🛡️

> An AI-powered Security Operations Center assistant that auto-triages, summarizes, and maps security alerts to MITRE ATT&CK — built to eliminate analyst alert fatigue.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-containerized-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The Problem: Alert Fatigue

Security Operations Center analysts can receive over **10,000 alerts per day** — each a raw, cryptic log line like:

```
[2024-03-10 02:14:55] ALERT - ET SCAN Possible Nmap User-Agent Observed - Source: 192.168.1.45
```

Analysts must read every alert, decide if it is a real threat or false positive, identify the attacker's technique, write a report, and respond — all manually, all day. This is **alert fatigue**, and it is one of the biggest unsolved problems in modern cybersecurity.

**SOCGPT** uses GPT-4 to automatically read these raw logs, summarize them in plain English, classify severity, map them to MITRE ATT&CK techniques, suggest first-response actions, and notify the SOC team — without a human reading each log individually.

---

## Architecture Overview

```
Raw Logs (Suricata / Zeek / Windows Event Logs)
        │
        ▼
[1] log_analysis.py    → Parses & structures raw log lines
        │
        ▼
[2] summarizer.py      → GPT-4 generates plain-English summary
        │
        ▼
[3] triage.py          → Classifies: LOW / MEDIUM / HIGH / CRITICAL
        │
        ▼
[4] mitre_mapper.py    → Maps to MITRE ATT&CK Technique ID
        │
        ▼
[5] remediation.py     → GPT-4 suggests first-response actions
        │
        ├──► [6] threat_explainer.py  → Analyst Q&A (natural language)
        │
        ▼
[7] notifier.py        → Email + Slack report delivery
        │
        ├──► api/main.py   → FastAPI REST endpoint (/analyze-log)
        └──► ui/app.py     → Streamlit web interface
```

---

## Features

| Feature | Description |
|---|---|
| AI Log Summarization | GPT-4 converts cryptic log lines into concise, factual 3-sentence summaries |
| Automated Triage | Classifies every alert as LOW / MEDIUM / HIGH / CRITICAL |
| MITRE ATT&CK Mapping | Maps log indicators to technique IDs (T1059, T1110, T1046, T1003, etc.) |
| AI Remediation Advice | GPT-4 suggests specific, actionable first-response steps per alert |
| Analyst Q&A | Ask natural language questions about any threat in a chat interface |
| Email Notifications | Sends HTML-formatted reports via SMTP with TLS encryption |
| Slack Alerts | Posts structured Block Kit messages to SOC Slack channels |
| REST API | FastAPI endpoint for integration with SIEM and automation pipelines |
| Web UI | Streamlit dashboard for file upload, analysis, and interactive results |
| Docker Ready | Containerized for one-command deployment on any infrastructure |

---

## Tech Stack

| Technology | Role | Why Chosen |
|---|---|---|
| Python 3.10 | Core language | Dominant in AI/ML; huge security ecosystem; rapid prototyping |
| GPT-4 (OpenAI) | AI brain | Superior cybersecurity knowledge; fewer hallucinations than GPT-3.5 |
| FastAPI | REST API layer | Async-native; handles concurrent OpenAI calls; auto-generates Swagger docs |
| Uvicorn | ASGI server | Runs FastAPI; handles async HTTP connections on port 8000 |
| Pydantic | Input validation | Type-safe API contracts; 422 errors on malformed input |
| Streamlit | Web UI | Pure Python UI; no HTML/CSS needed; built-in file upload and spinners |
| PyYAML | Configuration | Nested structured config with comments; safe_load prevents code execution |
| smtplib | Email sending | Built-in Python SMTP with STARTTLS encryption |
| Docker | Containerization | Portable deployment; eliminates environment inconsistencies |

---

## Project Structure

```
SOCGPT/
├── api/
│   └── main.py              # FastAPI REST endpoint — /analyze-log
├── src/
│   ├── log_analysis.py      # Log ingestion, parsing, and structuring
│   ├── summarizer.py        # GPT-4 plain-English summarization
│   ├── triage.py            # Severity classification (rule-based + LLM)
│   ├── mitre_mapper.py      # MITRE ATT&CK technique mapping
│   ├── remediation.py       # GPT-4 first-response suggestions
│   ├── threat_explainer.py  # Analyst Q&A with conversation history
│  
├── ui/
│   └── app.py               # Streamlit web interface
├── config/
│   └── settings.yaml        # Non-secret configuration (never commit secrets here)
├── data/
│   └── example_logs.txt     # Sample Suricata / Zeek / Windows Event logs
├── run_pipeline.py          # End-to-end orchestrator and demo script
├── requirements.txt         # Pinned Python dependencies
└── .gitignore               # Excludes .env, settings with secrets, __pycache__
```

---

## Installation

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/hemanshu1238/SOCGPT
cd SOCGPT

# Set your secrets
cp .env.example .env
# Edit .env and add your OpenAI API key and email credentials

# Build and run
docker build -t socgpt .
docker run -p 8501:8501 --env-file .env socgpt
```

Open `http://localhost:8501` in your browser.

### Option 2 — Local Python

```bash
git clone https://github.com/hemanshu1238/SOCGPT
cd SOCGPT

pip install -r requirements.txt

# Set your secrets
cp .env.example .env
# Edit .env

# Run the Streamlit UI
streamlit run ui/app.py

# Or run the REST API
uvicorn api.main:app --reload
```

---

## Configuration

**`config/settings.yaml`** — non-secret structured config:

```yaml
# Severity thresholds for rule-based triage
triage:
  critical_keywords: ["ransomware", "lateral movement", "mimikatz", "exploit"]
  high_keywords: ["powershell", "cmd.exe", "credential"]
  medium_keywords: ["port scan", "failed login", "nmap"]

# Email report settings
email:
  smtp_host: smtp.gmail.com
  smtp_port: 587

# OpenAI model settings
openai:
  model: gpt-4
  temperature: 0.3
  max_tokens: 500
```

**`.env`** — secrets only (never commit this):

```
OPENAI_API_KEY=sk-...
EMAIL_SENDER=soc@yourcompany.com
EMAIL_APP_PASSWORD=your-app-password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

> **Security note:** Always use `yaml.safe_load()` — never `yaml.load()`, which can execute arbitrary Python code from a malicious YAML file.

---

## REST API

Start the API server:

```bash
uvicorn api.main:app --reload
```

### `POST /analyze-log`

**Request:**

```json
{
  "log_text": "[2024-03-10 02:14:55] ALERT - ET SCAN Possible Nmap - Source: 192.168.1.45"
}
```

**Response:**

```json
{
  "summary": "A Suricata IDS alert detected a potential Nmap port scan from 192.168.1.45 targeting internal host 10.0.0.1. The scan pattern matches TCP SYN probing across multiple ports. This behavior is consistent with network reconnaissance, a common precursor to targeted exploitation.",
  "severity": "MEDIUM",
  "mitre": {
    "id": "T1046",
    "name": "Network Service Discovery"
  },
  "remediation": [
    "Block source IP 192.168.1.45 at the perimeter firewall.",
    "Review Suricata logs for additional scan patterns from this source.",
    "Check if 192.168.1.45 is a known internal asset performing authorized scanning.",
    "Enable geo-blocking if source IP resolves to an unexpected country."
  ]
}
```

Interactive API docs available at `http://localhost:8000/docs` (Swagger UI).

---

## How Each Module Works

### `log_analysis.py` — Log Ingestion & Parsing

Converts raw unstructured log text into structured Python dicts using `re` (regular expressions).

```python
import re

def parse_log(raw_line: str) -> dict:
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*' \
              r'(?P<src_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    match = re.search(pattern, raw_line)
    return {
        'raw': raw_line,
        'timestamp': match.group('timestamp') if match else None,
        'src_ip': match.group('src_ip') if match else None,
    }

def ingest_logs(filepath: str) -> list[dict]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return [parse_log(line) for line in f if line.strip()]
```

### `summarizer.py` — GPT-4 Summarization

Uses a precisely engineered system prompt to constrain GPT-4 to factual, SOC-appropriate output.

```python
import openai

SYSTEM_PROMPT = """You are a Tier-2 SOC analyst with expertise in network intrusion 
detection, endpoint security, and threat intelligence. When given a raw security log, 
produce a concise 3-sentence summary that:
1. Identifies the type of event
2. States the affected system and source
3. Indicates potential impact
Be factual. Do not speculate beyond what the log shows."""

def summarize(log_text: str) -> str:
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': log_text}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content
```

**Why temperature 0.3?** Security analysis requires consistent, reproducible outputs. High temperature would risk inventing threat indicators not present in the log.

### `triage.py` — Severity Classification

Hybrid approach: fast rule-based keyword matching first, with optional LLM-based contextual classification.

```python
SEVERITY_RULES = {
    'CRITICAL': ['ransomware', 'lateral movement', 'mimikatz', 'data exfiltration'],
    'HIGH':     ['powershell', 'cmd.exe', 'credential dump', 'privilege escalation'],
    'MEDIUM':   ['port scan', 'failed login', 'nmap', 'brute force'],
    'LOW':      ['dns query', 'http request', 'info']
}

def triage(log_text: str) -> str:
    log_lower = log_text.lower()
    for severity, keywords in SEVERITY_RULES.items():
        if any(kw in log_lower for kw in keywords):
            return severity
    return 'LOW'
```

### `mitre_mapper.py` — MITRE ATT&CK Mapping

Maps log indicators to MITRE ATT&CK technique IDs using a keyword lookup table.

```python
MITRE_MAPPINGS = {
    'powershell':             ('T1059.001', 'PowerShell'),
    'cmd.exe':                ('T1059.003', 'Windows Command Shell'),
    'login failed':           ('T1110',     'Brute Force'),
    'authentication failure': ('T1110',     'Brute Force'),
    'nmap':                   ('T1046',     'Network Service Discovery'),
    'mimikatz':               ('T1003',     'OS Credential Dumping'),
    'scheduled task':         ('T1053.005', 'Scheduled Task'),
    'new service':            ('T1543.003', 'Windows Service'),
}

def map_mitre(log_text: str) -> tuple:
    log_lower = log_text.lower()
    for keyword, technique in MITRE_MAPPINGS.items():
        if keyword in log_lower:
            return technique
    return ('Unknown', 'Technique not mapped')
```

### `notifier.py` — Email & Slack Alerts

**Email:** Uses `smtplib` with STARTTLS encryption on port 587.

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_report(to_email: str, subject: str, body_html: str):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings['email']['sender']
    msg['To'] = to_email
    msg.attach(MIMEText(body_html, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()   # Upgrade to encrypted TLS
        server.login(settings['email']['sender'], settings['email']['password'])
        server.sendmail(msg['From'], to_email, msg.as_string())
```

**Slack:** Uses Incoming Webhooks with Block Kit structured payload.

```python
import requests

def send_slack(webhook_url: str, alert: dict):
    payload = {
        'blocks': [
            {'type': 'header', 'text': {'type': 'plain_text', 'text': f'SOCGPT Alert: {alert["severity"]}'}},
            {'type': 'section', 'text': {'type': 'mrkdwn', 'text': f'*Summary:* {alert["summary"]}'}},
            {'type': 'section', 'fields': [
                {'type': 'mrkdwn', 'text': f'*MITRE:* {alert["mitre"]}'},
                {'type': 'mrkdwn', 'text': f'*Action:* {alert["remediation"]}'}
            ]}
        ]
    }
    requests.post(webhook_url, json=payload)
```

---

## Supported Log Formats

### Suricata (EVE JSON)

```json
{
  "event_type": "alert",
  "timestamp": "2024-03-10T02:14:55",
  "src_ip": "192.168.1.45",
  "dest_ip": "10.0.0.1",
  "alert": {
    "signature": "ET SCAN Possible Nmap User-Agent Observed",
    "severity": 2,
    "category": "Attempted Reconnaissance"
  }
}
```

### Windows Event Log (Security)

```
EventID: 4625
Source: Security
Message: An account failed to log on.
Logon Type: 3
Source Network Address: 192.168.1.45
Account Name: Administrator
```

### Zeek (conn.log)

```
1710036895.123456  C1234  192.168.1.45  45231  10.0.0.5  22  tcp  ssh  1.234  1024  512  SF
```

---

## MITRE ATT&CK Coverage

| Technique ID | Technique Name | Trigger Keywords |
|---|---|---|
| T1059.001 | PowerShell | powershell, psh |
| T1059.003 | Windows Command Shell | cmd.exe |
| T1110 | Brute Force | login failed, auth failure, repeated attempts |
| T1046 | Network Service Discovery | nmap, port scan |
| T1003 | OS Credential Dumping | mimikatz, lsass, credential dump |
| T1053.005 | Scheduled Task | schtasks, scheduled task |
| T1543.003 | Windows Service | new service, sc create |
| T1566 | Phishing | suspicious email, attachment |

---

## Security Considerations

### Protecting the Tool Itself

**API Key Security**
- Store `OPENAI_API_KEY` in `.env` — never in source code or `settings.yaml`
- Add `.env` to `.gitignore`
- Rotate API keys regularly; monitor usage for anomalies

**Log Data Privacy**
- Security logs contain sensitive internal IPs, hostnames, and usernames
- Sending logs to OpenAI means data leaves your network
- For high-security environments: replace GPT-4 with a self-hosted LLM (LLaMA 3 or Mistral via Ollama) to keep all data on-premise

**Prompt Injection**
- An attacker who controls log content could try to inject instructions into the GPT-4 prompt
- Mitigations: sanitize log input before prompt construction; use structured prompts that treat log content as data, not instructions; monitor for anomalous model outputs

**Rate Limiting**
- Add `slowapi` middleware to the FastAPI layer to prevent fake requests from exhausting your OpenAI token quota

**SSRF via Slack Webhooks**
- If webhook URLs are user-configurable, validate them against an allowlist to prevent Server-Side Request Forgery attacks targeting internal services

---

## Scaling to Production

The current design is single-process and synchronous. For enterprise-grade throughput (100,000+ alerts/day):

**Message Queue** — introduce RabbitMQ or Apache Kafka. Alerts are published to a topic; multiple worker processes consume asynchronously. Decouples ingestion rate from processing speed.

**Horizontal Scaling** — deploy multiple FastAPI worker instances behind a load balancer (Nginx or AWS ALB). Each instance handles API requests independently.

**Result Caching** — hash each log line (SHA256) and check Redis before calling OpenAI. Identical logs reuse cached results. Dramatically reduces API costs in environments with repeated alert signatures.

**Async Optimization** — replace synchronous OpenAI calls with `aiohttp` + `asyncio` for concurrent API calls within a single event loop.

**Persistent Storage** — store all analysis results in Elasticsearch (the `E` in the ELK stack) for querying, dashboarding, and historical pattern analysis.

---

## Roadmap

- [ ] **Local LLM (LLaMA 3 / Mistral)** — self-hosted via Ollama; zero data egress; fine-tune on org-specific log formats
- [ ] **Vector database** — ChromaDB/Pinecone for semantic similarity search against historical alerts
- [ ] **LangChain integration** — PromptTemplates, OutputParsers, Chains, and Memory for structured LLM orchestration
- [ ] **Kafka streaming** — real-time alert ingestion from Suricata/Zeek/Winlogbeat Kafka topics
- [ ] **MISP integration** — cross-reference IPs, domains, and hashes against threat intelligence feeds
- [ ] **Sigma rule generation** — auto-convert analysis into deployable Sigma detection rules
- [ ] **JWT authentication + RBAC** — analyst / manager / admin roles on the FastAPI layer
- [ ] **SOAR integration** — automated remediation via CrowdStrike/SentinelOne EDR API and ServiceNow ticketing
- [ ] **Evaluation pipeline** — BLEU/ROUGE scoring, hallucination detection, and A/B testing vs GPT-3.5-turbo

---

## Quick Reference — Concepts

| Term | One-Line Explanation |
|---|---|
| Alert fatigue | Analyst overwhelm from too many alerts; core problem SOCGPT solves |
| GPT-4 | LLM by OpenAI; transformer architecture; used for summarization and remediation |
| Temperature | OpenAI param 0–2; 0.3 used for consistent, factual security analysis |
| System prompt | First message to GPT-4 setting persona and output constraints |
| Prompt injection | Attack where malicious log content manipulates LLM behavior |
| FastAPI | Async Python web framework; built on Starlette + Pydantic |
| Uvicorn | ASGI server that runs FastAPI; handles async HTTP connections |
| Pydantic | Data validation via type hints; enforces API request contracts |
| Streamlit | Python browser UI framework; no HTML/CSS required |
| MITRE ATT&CK | Framework of adversary tactics (why) and techniques (how); T-coded IDs |
| Suricata | Open-source NIDS/NIPS; generates EVE JSON alerts |
| Zeek | Network analysis framework; rich structured logs (conn, dns, http, ssl) |
| IDS vs IPS | IDS = detect only (passive); IPS = detect + block (active/inline) |
| False positive | Alert fires but no real attack; contributes to alert fatigue |
| False negative | Real attack with no alert; most dangerous security failure |
| STARTTLS | Upgrades plain SMTP to encrypted TLS on port 587 |
| SSRF | Server-Side Request Forgery; validate webhook URLs against allowlist |
| Exponential backoff | Retry strategy: wait 2^n seconds on failure to prevent API overload |
| SOAR | Security Orchestration, Automation and Response; automates incident workflows |
| Vector DB | Semantic similarity search using embeddings (ChromaDB, Pinecone) |

---

## Author

**Hemanshu Tyagi**
B.E. Computer Science Engineering — Chitkara University (2023–2027)
Specialization: Cybersecurity — Network Security, Application Security, VAPT, OWASP Top 10

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/hemanshu-tyagi-519b6236a)
[![GitHub](https://img.shields.io/badge/GitHub-hemanshu1238-black)](https://github.com/hemanshu1238)

---

## Related Projects

- [EmailAnalyzer](https://github.com/hemanshu1238/-EmailAnalyzer) — Python CLI tool for phishing email forensics; extracts headers, hashes, links, and attachments from .eml files with VirusTotal/AbuseIPDB/UrlScan investigation links

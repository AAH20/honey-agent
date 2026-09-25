"""
Data models and schemas for Honey-Agent decoy vault and injection tripwires.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import time


class HoneyTokenType(str, Enum):
    AWS_CREDENTIAL = "aws_credential"
    BROWSER_COOKIE = "browser_cookie"
    SSH_KEY = "ssh_key"
    VAULT_PASSWORD = "vault_password"
    ENV_SECRET = "env_secret"
    CANARY_FILE = "canary_file"


@dataclass
class HoneyToken:
    token_id: str
    token_type: HoneyTokenType
    decoy_path: str
    synthetic_secret: str
    fingerprint_hmac: str
    is_tripped: bool = False
    tripped_at: Optional[float] = None
    created_at: float = field(default_factory=time.time)


@dataclass
class TripwireEvent:
    event_id: str
    timestamp: float
    token_id: str
    token_type: HoneyTokenType
    accessing_agent: str
    attempted_action: str  # "read_file", "curl_exfil", "type_secret", "click_vault"
    payload_snippet: str
    quarantine_active: bool = True
    detection_latency_ms: float = 0.0


@dataclass
class ForensicReport:
    report_id: str
    timestamp: float
    threat_severity: str  # "CRITICAL", "HIGH"
    attack_vector: str    # "INDIRECT_PROMPT_INJECTION"
    compromised_honeytoken: str
    attacker_payload: str
    containment_status: str  # "CONTAINER_FROZEN", "NETWORK_SEVERED"
    sentinel_model: str = "Gemini 3.8 Flash Cyber"
    remediation_advice: str = ""

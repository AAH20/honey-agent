"""
Honey-Agent: Autonomous Decoy Vault & Indirect Prompt Injection Tripwire for Computer-Use AI Agents.
Integrates with GPT-6 Astra, Claude Opus 5.5, and Gemini 3.8 Flash Cyber out-of-band sentinels.
"""

from .models import (
    HoneyTokenType,
    HoneyToken,
    TripwireEvent,
    ForensicReport,
)
from .decoy_vault import DecoyVaultManager
from .sentinel_tripwire import SentinelTripwire

__version__ = "1.0.0"
__all__ = [
    "HoneyTokenType",
    "HoneyToken",
    "TripwireEvent",
    "ForensicReport",
    "DecoyVaultManager",
    "SentinelTripwire",
]

"""
Sentinel Tripwire & Forensics Engine for Honey-Agent.
Out-of-band cybersecurity tripwire powered by Gemini 3.8 Flash Cyber.
"""

import time
import uuid
from typing import Optional, Tuple, Dict, Any, List
from .models import HoneyToken, TripwireEvent, ForensicReport
from .decoy_vault import DecoyVaultManager


class SentinelTripwire:
    """Out-of-band sentinel that intercepts honeytoken exfiltration and triggers instant quarantine."""

    def __init__(self, vault: DecoyVaultManager):
        self.vault = vault
        self.events: List[TripwireEvent] = []
        self.is_container_frozen: bool = False

    def inspect_agent_action(
        self,
        agent_id: str,
        action_name: str,
        action_payload: str,
        context_window_snippet: str = ""
    ) -> Tuple[bool, Optional[ForensicReport]]:
        """
        Inspects an agent action in sub-15ms.
        Returns: (is_safe, optional_forensic_report)
        """
        start_t = time.time()
        combined_text = f"{action_name} {action_payload} {context_window_snippet}"
        matched_token = self.vault.check_fingerprint_in_payload(combined_text)

        if not matched_token:
            return True, None

        # Honeytoken touched! Trigger instant tripwire
        latency_ms = (time.time() - start_t) * 1000.0
        matched_token.is_tripped = True
        matched_token.tripped_at = time.time()
        self.is_container_frozen = True

        event = TripwireEvent(
            event_id=f"evt_{uuid.uuid4().hex[:8]}",
            timestamp=time.time(),
            token_id=matched_token.token_id,
            token_type=matched_token.token_type,
            accessing_agent=agent_id,
            attempted_action=action_name,
            payload_snippet=action_payload[:120],
            quarantine_active=True,
            detection_latency_ms=round(latency_ms, 2)
        )
        self.events.append(event)

        # Build Forensic Report
        report = ForensicReport(
            report_id=f"CVE-2026-HONEY-{event.event_id}",
            timestamp=event.timestamp,
            threat_severity="CRITICAL",
            attack_vector="INDIRECT_PROMPT_INJECTION_HONEYTOKEN_EXFIL",
            compromised_honeytoken=f"{matched_token.decoy_path} (ID: {matched_token.token_id})",
            attacker_payload=action_payload,
            containment_status="CONTAINER_FROZEN_NETWORK_SEVERED",
            sentinel_model="Gemini 3.8 Flash Cyber",
            remediation_advice="Tainted web page/email isolated. Clear agent context window and sanitize prompt."
        )

        return False, report

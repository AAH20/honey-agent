"""
Decoy Vault Engine for Honey-Agent.
Seeds synthetic honeytokens with cryptographic HMAC fingerprints into agent environments.
"""

import hmac
import hashlib
import time
from typing import Dict, List, Optional
from .models import HoneyToken, HoneyTokenType


class DecoyVaultManager:
    """Provisions and registers cryptographic honeytokens across desktop, filesystem, and browser."""

    def __init__(self, master_key: str = "sovereign_cyber_honey_key_2026"):
        self.master_key = master_key.encode("utf-8")
        self.registry: Dict[str, HoneyToken] = {}
        self._init_default_decoys()

    def _generate_hmac(self, token_id: str, seed: str) -> str:
        """Computes cryptographic HMAC fingerprint for a decoy secret."""
        msg = f"{token_id}:{seed}".encode("utf-8")
        return hmac.new(self.master_key, msg, hashlib.sha256).hexdigest()[:16]

    def register_honeytoken(
        self,
        token_id: str,
        token_type: HoneyTokenType,
        decoy_path: str,
        raw_secret_template: str
    ) -> HoneyToken:
        """Creates a honeytoken with embedded HMAC signature and registers it."""
        fingerprint = self._generate_hmac(token_id, decoy_path)
        synthetic_secret = raw_secret_template.replace("{SIG}", fingerprint)

        token = HoneyToken(
            token_id=token_id,
            token_type=token_type,
            decoy_path=decoy_path,
            synthetic_secret=synthetic_secret,
            fingerprint_hmac=fingerprint
        )
        self.registry[token_id] = token
        return token

    def _init_default_decoys(self) -> None:
        """Seeds standard high-value targets commonly hunted by prompt injectors."""
        # 1. AWS Credentials
        self.register_honeytoken(
            token_id="honey_aws_keys",
            token_type=HoneyTokenType.AWS_CREDENTIAL,
            decoy_path="~/.aws/credentials",
            raw_secret_template="AKIA{SIG}EXAMPLETRAIL:wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
        )

        # 2. Production .env Secret
        self.register_honeytoken(
            token_id="honey_env_secret",
            token_type=HoneyTokenType.ENV_SECRET,
            decoy_path="/workspace/.env.production",
            raw_secret_template="DATABASE_URL=postgres://admin:sk_live_{SIG}@db.internal:5432/prod"
        )

        # 3. Browser Decoy Password Vault
        self.register_honeytoken(
            token_id="honey_browser_vault",
            token_type=HoneyTokenType.VAULT_PASSWORD,
            decoy_path="Chromium://passwords/cloud_portal",
            raw_secret_template="master_admin_pass_{SIG}#$!"
        )

    def check_fingerprint_in_payload(self, text: str) -> Optional[HoneyToken]:
        """Scans arbitrary text or network requests for any honeytoken secret or fingerprint."""
        for token in self.registry.values():
            if token.fingerprint_hmac in text or token.synthetic_secret in text:
                return token
            if token.decoy_path in text and ("cat " in text or "curl " in text or "open " in text):
                return token
        return None

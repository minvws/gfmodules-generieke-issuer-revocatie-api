import json
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from jwt.utils import base64url_decode

from app.config import ConfigCredential
from app.services.bitstring import generate_compressed_bitstring
from app.services.revokation_service import RevocationService


class VerifiableCredentialGenerator:
    def __init__(self, config: ConfigCredential, revocation_service: RevocationService):
        self.config = config
        self.revocation_service = revocation_service

        # read path
        if not self.config.private_key_jwk:
            raise ValueError("Private key JWK must be provided in the configuration")

        # Load the private key content from JWK file
        try:
            with open(self.config.private_key_jwk, "r") as f:
                jwk_content = f.read()

                self._jwk = json.loads(jwk_content)
                if self._jwk["kty"] != "OKP" or self._jwk["crv"] != "Ed25519":
                    raise ValueError("Invalid JWK: must be an Ed25519 key")

                private_bytes = base64url_decode(self._jwk["d"])
                self._private_key = Ed25519PrivateKey.from_private_bytes(private_bytes)

        except Exception as e:
            raise ValueError(f"Failed to load private key JWK: {e}")

    def generate(self) -> str:
        idx_list = self.revocation_service.get_revoked_indices()
        bs = generate_compressed_bitstring(idx_list, self.config.bitstring_size_kb)

        id = uuid.uuid4()

        # vc = {
        #     "@context": ["https://www.w3.org/ns/credentials/v2"],
        #     "id": str(id),
        #     "type": ["VerifiableCredential", "BitstringStatusListCredential"],
        #     "issuer": self.config.did,
        #     "validFrom": "2023-01-01T00:00:00Z",
        #     "validUntil": "2028-01-01T00:00:00Z",
        #     "credentialSubject": {
        #         "id": str(id),
        #         "type": "BitstringStatusList",
        #         "statusPurpose": "revocation",
        #         "encodedList": bs,
        #     },
        # }

        # 2021 version deluxe
        vc = {
            "@context": ["https://www.w3.org/2018/credentials/v1", "https://w3id.org/vc/status-list/2021/v1"],
            "id": str(id),
            "type": ["VerifiableCredential", "StatusList2021Credential"],
            "issuer": self.config.did,
            "issued": "2023-01-01T00:00:00Z",
            "credentialSubject": {
                "id": str(id),
                "type": "StatusList2021",
                "statusPurpose": "revocation",
                "encodedList": bs,
            },
        }

        now = datetime.now(timezone.utc)

        payload = {
            "nbf": int(datetime.fromisoformat(vc["issued"].replace("Z", "+00:00")).timestamp()),  # type: ignore
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=3600)).timestamp()),
            "vc": vc,
        }

        headers = {
            "iss": vc["issuer"],
            "jti": str(id),
        }

        return jwt.encode(payload, self._private_key, algorithm="EdDSA", headers=headers)

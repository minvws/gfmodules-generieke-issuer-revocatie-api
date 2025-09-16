import base64
import hashlib
import json
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def generate_did_jwk(public_jwk: dict[str, str]) -> str:
    jwk_json = json.dumps(public_jwk, separators=(",", ":"), sort_keys=True)
    jwk_bytes = jwk_json.encode("utf-8")
    jwk_b64 = base64url_encode(jwk_bytes)
    return f"did:jwk:{jwk_b64}"


def compute_kid(jwk: dict[str, str]) -> str:
    thumbprint_dict = {"crv": jwk["crv"], "kty": jwk["kty"], "x": jwk["x"]}

    thumbprint_json = json.dumps(thumbprint_dict, separators=(",", ":"), sort_keys=True)
    thumbprint_bytes = thumbprint_json.encode("utf-8")

    digest = hashlib.sha256(thumbprint_bytes).digest()
    return base64url_encode(digest)


private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption(),
)
public_bytes = public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)

jwk = {
    "kty": "OKP",
    "d": base64url_encode(private_bytes),
    "use": "sig",
    "crv": "Ed25519",
    "x": base64url_encode(public_bytes),
    "alg": "EdDSA",
}
jwk["kid"] = compute_kid(jwk)

public_jwk = {k: v for k, v in jwk.items() if k != "d"}

print("-- JWK -----------------------------------\n")
print(json.dumps(jwk, indent=2), "\n")
print("------------------------------------------\n")


print("-- DID -----------------------------------\n")
print(generate_did_jwk(public_jwk), "\n")
print("------------------------------------------\n")

if len(sys.argv) == 2:
    with open(sys.argv[1], "w") as f:
        print(f"Putting the JWK in {sys.argv[1]}")
        f.write(json.dumps(jwk, indent=2) + "\n")

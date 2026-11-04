#!/usr/bin/env python3
"""
TimesheetSeal — Local-first crew timesheet and hours evidence sealer.
Offline. Deterministic. Pay once.
Compatible with QuantumGuard CONTRACT-v1.
"""

import argparse
import json
import hashlib
import base64
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO = True
except ImportError:
    CRYPTO = False

CONTRACT_VERSION = "1"
ALG = "ed25519"

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_or_generate_key(key_path: str = "timesheetseal_key.pem"):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        return priv
    if not CRYPTO:
        raise SystemExit("cryptography package required for signing. pip install cryptography")
    priv = ed25519.Ed25519PrivateKey.generate()
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(key_path, "wb") as f:
        f.write(pem)
    print(f"Generated new key: {key_path}")
    return priv

def get_public_key_hex(priv):
    raw = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return raw.hex()

def sign_payload(priv, payload_hash: bytes) -> str:
    sig = priv.sign(payload_hash)
    return sig.hex()

def build_payload(timesheet: dict) -> bytes:
    # Canonical JSON for determinism
    canonical = json.dumps(timesheet, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return canonical

def seal_timesheet(timesheet: dict, priv, out_path: str):
    payload = build_payload(timesheet)
    payload_hash = hashlib.sha256(payload).digest()
    payload_hash_hex = payload_hash.hex()
    signature = sign_payload(priv, payload_hash)
    public_key = get_public_key_hex(priv)

    bundle = {
        "version": CONTRACT_VERSION,
        "payload": base64.b64encode(payload).decode("ascii"),
        "payload_hash": payload_hash_hex,
        "signature": signature,
        "public_key": public_key,
        "alg": ALG,
    }
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed timesheet written to {out_path}")
    print(f"Verify with: qg verify {out_path}")

def demo_timesheet():
    return {
        "type": "crew_timesheet",
        "job_id": "JOB-2026-042",
        "site": "Site Alpha — Springfield, MO",
        "date": "2026-11-04",
        "crew": [
            {
                "name": "Operator A",
                "role": "Lead",
                "regular_hours": 8.0,
                "overtime_hours": 1.5,
                "break_minutes": 30,
                "job_codes": ["INSTALL", "CONDUIT"]
            },
            {
                "name": "Operator B",
                "role": "Tech",
                "regular_hours": 7.5,
                "overtime_hours": 0.0,
                "break_minutes": 30,
                "job_codes": ["INSTALL"]
            }
        ],
        "total_regular": 15.5,
        "total_overtime": 1.5,
        "notes": "Overtime approved by client on-site.",
        "approved_by": "Client Rep",
        "sealed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": "TimesheetSeal/0.1.0"
    }

def main():
    parser = argparse.ArgumentParser(description="TimesheetSeal — seal crew timesheets into QuantumGuard packs.")
    parser.add_argument("--demo", action="store_true", help="Run demo and seal sample timesheet")
    parser.add_argument("--json", help="Path to JSON timesheet file to seal")
    parser.add_argument("--out", default="sealed-timesheet.json", help="Output sealed bundle path")
    parser.add_argument("--key", default="timesheetseal_key.pem", help="Path to Ed25519 private key PEM")
    args = parser.parse_args()

    if args.demo:
        timesheet = demo_timesheet()
        print("Demo timesheet:")
        print(json.dumps(timesheet, indent=2))
    elif args.json:
        with open(args.json) as f:
            timesheet = json.load(f)
    else:
        parser.print_help()
        return

    priv = load_or_generate_key(args.key)
    seal_timesheet(timesheet, priv, args.out)

if __name__ == "__main__":
    main()

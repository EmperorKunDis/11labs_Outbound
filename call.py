#!/usr/bin/env python3
import argparse
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID", "agent_9501kq9tn9nkfm3rbwtfjr4c9jfw")
API_KEY = os.getenv("ELEVENLABS_API_KEY")
PHONE_NUMBER_ID = os.getenv("ELEVENLABS_PHONE_NUMBER_ID")


def call(to_number: str, name: str | None, company: str | None) -> None:
    if not API_KEY:
        sys.exit("Chybí ELEVENLABS_API_KEY v .env")
    if not PHONE_NUMBER_ID:
        sys.exit("Chybí ELEVENLABS_PHONE_NUMBER_ID v .env")

    payload: dict = {
        "agent_id": AGENT_ID,
        "agent_phone_number_id": PHONE_NUMBER_ID,
        "to_number": to_number,
    }

    dynamic_vars: dict = {}
    if name:
        dynamic_vars["caller_name"] = name
    if company:
        dynamic_vars["caller_company"] = company
    if dynamic_vars:
        payload["conversation_initiation_client_data"] = {
            "dynamic_variables": dynamic_vars
        }

    resp = requests.post(
        "https://api.elevenlabs.io/v1/convai/twilio/outbound-call",
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
        json=payload,
        timeout=15,
    )

    if not resp.ok:
        sys.exit(f"Chyba {resp.status_code}: {resp.text}")

    data = resp.json()
    print(f"✓ Hovor zahájen → {to_number}")
    if data.get("conversation_id"):
        print(f"  conversation_id: {data['conversation_id']}")
    if data.get("callSid"):
        print(f"  callSid: {data['callSid']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spustí odchozí hovor se Stelou (VELYOS)"
    )
    parser.add_argument(
        "number", help="Telefonní číslo v mezinárodním formátu, např. +420777123456"
    )
    parser.add_argument("--name", help="Jméno volané osoby (volitelné)")
    parser.add_argument("--company", help="Název firmy (volitelné)")
    args = parser.parse_args()

    call(args.number, args.name, args.company)

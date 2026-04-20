#!/usr/bin/env python3
"""
EV / Hybrid Fault Family Lookup
Searches curated OEM-neutral and OEM-specific EV fault families for high-voltage
battery, inverter, charge, and thermal system diagnosis.

Usage:
  python3 ev_fault_lookup.py search <keyword>
  python3 ev_fault_lookup.py oem <brand> <code-or-family>
  python3 ev_fault_lookup.py system <hv_battery|inverter|charge|thermal>
  python3 ev_fault_lookup.py --json <any command>
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "ev_fault_families.json"
SYSTEMS = {"hv_battery", "inverter", "charge", "thermal"}


def normalize(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def normalize_token(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def load_families() -> List[Dict]:
    with open(DATA_FILE, encoding="utf-8") as handle:
        families = json.load(handle)
    if not isinstance(families, list):
        raise ValueError("EV fault family data must be a list")
    return families


def family_matches_code(family: Dict, code_or_family: str) -> bool:
    needle = normalize_token(code_or_family)
    haystacks = [family.get("family", "")]
    haystacks.extend(family.get("family_prefixes", []))
    for item in haystacks:
        token = normalize_token(item)
        if token and (needle == token or needle.startswith(token) or token.startswith(needle)):
            return True
    return False


def search_families(keyword: str, families: List[Dict]) -> List[Dict]:
    needle = normalize_token(keyword)
    results = []
    for family in families:
        parts = [
            family.get("oem", ""),
            family.get("family", ""),
            family.get("meaning", ""),
            " ".join(family.get("keywords", [])),
            " ".join(family.get("likely_causes", [])),
        ]
        haystack = normalize_token(" ".join(parts))
        if needle in haystack:
            results.append(family)
    return results


def filter_by_system(system: str, families: List[Dict]) -> List[Dict]:
    return [family for family in families if family.get("system") == system]


def lookup_by_oem(oem: str, code_or_family: str, families: List[Dict]) -> Optional[Dict]:
    brand = normalize(oem)
    candidates = [family for family in families if normalize(family.get("oem", "")) == brand]
    for family in candidates:
        if family_matches_code(family, code_or_family):
            return family
    return None


def format_family(family: Dict) -> str:
    lines = [
        f"OEM: {family['oem']}",
        f"Family: {family['family']}",
        f"System: {family['system']}",
        f"Meaning: {family['meaning']}",
        "Common Prefixes:",
    ]
    for prefix in family.get("family_prefixes", []):
        lines.append(f"  - {prefix}")
    lines.append("Likely Causes:")
    for cause in family.get("likely_causes", []):
        lines.append(f"  - {cause}")
    lines.append("Low-Risk Checks:")
    for check in family.get("low_risk_checks", []):
        lines.append(f"  - {check}")
    lines.append(f"Escalation: {family['escalation']}")
    return "\n".join(lines)


def usage() -> str:
    return (
        "Usage:\n"
        "  python3 ev_fault_lookup.py search <keyword>\n"
        "  python3 ev_fault_lookup.py oem <brand> <code-or-family>\n"
        "  python3 ev_fault_lookup.py system <hv_battery|inverter|charge|thermal>\n"
        "  python3 ev_fault_lookup.py --json <any command>"
    )


def main() -> int:
    if len(sys.argv) < 2:
        print(usage())
        return 1

    output_json = "--json" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--json"]

    try:
        families = load_families()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Failed to load EV fault family data: {exc}", file=sys.stderr)
        return 1

    command = args[0].lower()

    if command == "search" and len(args) >= 2:
        keyword = " ".join(args[1:])
        results = search_families(keyword, families)
        if output_json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Search results for '{keyword}' ({len(results)} found):\n")
            for family in results:
                print(format_family(family))
                print("---")
            if not results:
                print("No EV fault families found. Try a different keyword.")
        return 0

    if command == "oem" and len(args) >= 3:
        brand = args[1]
        code_or_family = " ".join(args[2:])
        result = lookup_by_oem(brand, code_or_family, families)
        if not result:
            print(f"No EV fault family match for OEM '{brand}' and query '{code_or_family}'.")
            return 1
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_family(result))
        return 0

    if command == "system" and len(args) >= 2:
        system = args[1].lower()
        if system not in SYSTEMS:
            print(f"Invalid system '{system}'. Expected one of: {', '.join(sorted(SYSTEMS))}.")
            return 1
        results = filter_by_system(system, families)
        if output_json:
            print(json.dumps(results, indent=2))
        else:
            print(f"EV fault families for system '{system}' ({len(results)} found):\n")
            for family in results:
                print(format_family(family))
                print("---")
        return 0

    print(usage())
    return 1


if __name__ == "__main__":
    sys.exit(main())

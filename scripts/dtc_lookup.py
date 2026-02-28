#!/usr/bin/env python3
"""
DTC (Diagnostic Trouble Code) Lookup Tool
Looks up OBD-II diagnostic trouble codes from the Wal33D open-source database.
Falls back to built-in common codes if network unavailable.

Usage:
  python3 dtc_lookup.py P0300           # Single code lookup
  python3 dtc_lookup.py P0300 P0171     # Multiple codes
  python3 dtc_lookup.py --search misfire # Search by keyword
  python3 dtc_lookup.py --system engine  # List codes by system
"""

import sys
import json
import os
import urllib.request
import urllib.error
import re
from pathlib import Path

CACHE_DIR = Path(os.environ.get("DIAG_DATA_DIR", Path.home() / ".vehicle-diagnostics"))
CACHE_FILE = CACHE_DIR / "dtc_cache.json"

# Wal33D DTC database raw URLs (GitHub)
DTC_URLS = {
    "generic": "https://raw.githubusercontent.com/AurelienMusic/obd2-dtc-database/main/dtc_database.json",
    "backup": "https://raw.githubusercontent.com/Wal33D/obd2-dtc/main/src/data/genericDTC.json"
}

# Built-in common codes (fallback when offline)
COMMON_CODES = {
    "P0100": {"desc": "Mass Air Flow (MAF) Circuit Malfunction", "system": "fuel_air", "severity": "moderate",
              "causes": ["Dirty/faulty MAF sensor", "Air leak between MAF and throttle body", "Damaged MAF wiring"],
              "fixes": ["Clean MAF sensor with MAF cleaner spray", "Inspect air intake duct for cracks", "Check MAF connector and wiring"]},
    "P0101": {"desc": "Mass Air Flow (MAF) Circuit Range/Performance", "system": "fuel_air", "severity": "moderate",
              "causes": ["Dirty MAF sensor", "Vacuum leak", "Restricted air filter"],
              "fixes": ["Clean or replace MAF sensor", "Check for vacuum leaks", "Replace air filter"]},
    "P0128": {"desc": "Coolant Thermostat Below Thermostat Regulating Temperature", "system": "cooling", "severity": "low",
              "causes": ["Stuck-open thermostat", "Low coolant level", "Faulty coolant temp sensor"],
              "fixes": ["Replace thermostat", "Check and top off coolant", "Test coolant temp sensor"]},
    "P0131": {"desc": "O2 Sensor Circuit Low Voltage (Bank 1 Sensor 1)", "system": "fuel_air", "severity": "moderate",
              "causes": ["Faulty O2 sensor", "Exhaust leak before sensor", "Wiring issue"],
              "fixes": ["Replace Bank 1 Sensor 1 O2 sensor", "Inspect exhaust manifold for leaks", "Check O2 sensor wiring"]},
    "P0171": {"desc": "System Too Lean (Bank 1)", "system": "fuel_air", "severity": "moderate",
              "causes": ["Vacuum leak", "Dirty MAF sensor", "Weak fuel pump", "Clogged fuel filter", "Faulty PCV valve"],
              "fixes": ["Smoke test for vacuum leaks", "Clean MAF sensor", "Check fuel pressure", "Replace PCV valve"]},
    "P0174": {"desc": "System Too Lean (Bank 2)", "system": "fuel_air", "severity": "moderate",
              "causes": ["Vacuum leak on bank 2 side", "Dirty MAF sensor", "Intake manifold gasket leak"],
              "fixes": ["Smoke test for vacuum leaks", "Clean MAF sensor", "Inspect intake manifold gaskets"]},
    "P0300": {"desc": "Random/Multiple Cylinder Misfire Detected", "system": "ignition", "severity": "high",
              "causes": ["Worn spark plugs", "Faulty ignition coils", "Vacuum leak", "Low fuel pressure", "EGR valve issue"],
              "fixes": ["Replace spark plugs", "Test/replace ignition coils", "Check for vacuum leaks", "Test fuel pressure"]},
    "P0301": {"desc": "Cylinder 1 Misfire Detected", "system": "ignition", "severity": "high",
              "causes": ["Bad spark plug cyl 1", "Faulty coil pack cyl 1", "Injector cyl 1 issue", "Low compression cyl 1"],
              "fixes": ["Replace spark plug cyl 1", "Swap coil packs to test", "Test injector", "Compression test"]},
    "P0302": {"desc": "Cylinder 2 Misfire Detected", "system": "ignition", "severity": "high",
              "causes": ["Bad spark plug cyl 2", "Faulty coil pack cyl 2", "Injector cyl 2 issue"],
              "fixes": ["Replace spark plug cyl 2", "Swap coil packs to test", "Test injector"]},
    "P0303": {"desc": "Cylinder 3 Misfire Detected", "system": "ignition", "severity": "high",
              "causes": ["Bad spark plug cyl 3", "Faulty coil pack cyl 3", "Injector cyl 3 issue"],
              "fixes": ["Replace spark plug cyl 3", "Swap coil packs to test", "Test injector"]},
    "P0304": {"desc": "Cylinder 4 Misfire Detected", "system": "ignition", "severity": "high",
              "causes": ["Bad spark plug cyl 4", "Faulty coil pack cyl 4", "Injector cyl 4 issue"],
              "fixes": ["Replace spark plug cyl 4", "Swap coil packs to test", "Test injector"]},
    "P0325": {"desc": "Knock Sensor 1 Circuit Malfunction", "system": "ignition", "severity": "moderate",
              "causes": ["Faulty knock sensor", "Wiring issue", "Incorrect torque on sensor"],
              "fixes": ["Replace knock sensor", "Check wiring harness", "Torque sensor to spec"]},
    "P0340": {"desc": "Camshaft Position Sensor Circuit Malfunction", "system": "ignition", "severity": "high",
              "causes": ["Faulty cam position sensor", "Damaged tone ring", "Wiring issue", "Timing chain stretched"],
              "fixes": ["Replace cam position sensor", "Inspect tone ring", "Check wiring", "Check timing chain"]},
    "P0401": {"desc": "EGR Flow Insufficient Detected", "system": "emissions", "severity": "low",
              "causes": ["Clogged EGR passages", "Faulty EGR valve", "Carbon buildup"],
              "fixes": ["Clean EGR valve and passages", "Replace EGR valve", "Clean intake manifold carbon"]},
    "P0420": {"desc": "Catalyst System Efficiency Below Threshold (Bank 1)", "system": "emissions", "severity": "moderate",
              "causes": ["Failed catalytic converter", "Exhaust leak", "Faulty downstream O2 sensor", "Engine misfire damaging cat"],
              "fixes": ["Replace catalytic converter", "Fix exhaust leaks", "Replace downstream O2 sensor", "Fix root cause misfire first"]},
    "P0430": {"desc": "Catalyst System Efficiency Below Threshold (Bank 2)", "system": "emissions", "severity": "moderate",
              "causes": ["Failed catalytic converter bank 2", "Exhaust leak", "Faulty downstream O2 sensor bank 2"],
              "fixes": ["Replace catalytic converter bank 2", "Fix exhaust leaks", "Replace downstream O2 sensor bank 2"]},
    "P0440": {"desc": "Evaporative Emission Control System Malfunction", "system": "emissions", "severity": "low",
              "causes": ["Loose or damaged gas cap", "EVAP canister leak", "Purge valve stuck"],
              "fixes": ["Tighten or replace gas cap", "Smoke test EVAP system", "Replace purge valve"]},
    "P0442": {"desc": "EVAP System Leak Detected (Small Leak)", "system": "emissions", "severity": "low",
              "causes": ["Loose gas cap", "Cracked EVAP hose", "Faulty purge valve", "Leaking EVAP canister"],
              "fixes": ["Replace gas cap", "Smoke test EVAP system", "Replace purge/vent valve"]},
    "P0446": {"desc": "EVAP Vent Control Circuit Malfunction", "system": "emissions", "severity": "low",
              "causes": ["Faulty vent valve", "Blocked vent line", "Wiring issue"],
              "fixes": ["Replace vent valve", "Clear blockage in vent line", "Check wiring"]},
    "P0455": {"desc": "EVAP System Leak Detected (Large Leak)", "system": "emissions", "severity": "low",
              "causes": ["Gas cap left off or severely damaged", "Disconnected EVAP hose", "Cracked EVAP canister"],
              "fixes": ["Replace gas cap", "Inspect all EVAP hoses", "Check EVAP canister"]},
    "P0500": {"desc": "Vehicle Speed Sensor Malfunction", "system": "transmission", "severity": "moderate",
              "causes": ["Faulty VSS", "Damaged wiring", "Faulty TCM/PCM connection"],
              "fixes": ["Replace vehicle speed sensor", "Inspect wiring to VSS", "Check connections"]},
    "P0505": {"desc": "Idle Air Control System Malfunction", "system": "fuel_air", "severity": "moderate",
              "causes": ["Dirty IAC valve", "Vacuum leak", "Throttle body carbon buildup"],
              "fixes": ["Clean or replace IAC valve", "Check for vacuum leaks", "Clean throttle body"]},
    "P0507": {"desc": "Idle Control System RPM Higher Than Expected", "system": "fuel_air", "severity": "low",
              "causes": ["Vacuum leak", "Dirty throttle body", "Faulty IAC valve"],
              "fixes": ["Check for vacuum leaks", "Clean throttle body", "Replace IAC valve"]},
    "P0700": {"desc": "Transmission Control System Malfunction", "system": "transmission", "severity": "high",
              "causes": ["TCM fault", "Wiring issue", "Internal transmission problem"],
              "fixes": ["Scan for transmission-specific codes", "Check transmission wiring", "Inspect transmission"]},
    "P0715": {"desc": "Input/Turbine Speed Sensor Circuit Malfunction", "system": "transmission", "severity": "high",
              "causes": ["Faulty input speed sensor", "Damaged wiring", "Low transmission fluid"],
              "fixes": ["Replace input speed sensor", "Check wiring", "Check/top off transmission fluid"]},
    "P0720": {"desc": "Output Speed Sensor Circuit Malfunction", "system": "transmission", "severity": "high",
              "causes": ["Faulty output speed sensor", "Damaged wiring", "Internal transmission damage"],
              "fixes": ["Replace output speed sensor", "Check wiring", "Inspect transmission"]},
    "P0741": {"desc": "Torque Converter Clutch Circuit Performance or Stuck Off", "system": "transmission", "severity": "high",
              "causes": ["Faulty TCC solenoid", "Dirty transmission fluid", "Internal transmission wear"],
              "fixes": ["Replace TCC solenoid", "Flush transmission fluid", "Rebuild transmission if internal"]},
    "C0035": {"desc": "Left Front Wheel Speed Sensor Circuit", "system": "abs", "severity": "moderate",
              "causes": ["Faulty wheel speed sensor", "Damaged tone ring", "Wiring issue"],
              "fixes": ["Replace wheel speed sensor", "Inspect tone ring for damage", "Check wiring harness"]},
    "B0100": {"desc": "Electronic Frontal Sensor 1 Malfunction", "system": "body", "severity": "high",
              "causes": ["Faulty crash sensor", "Wiring damage", "Previous collision damage"],
              "fixes": ["Replace frontal sensor", "Inspect wiring", "Check for frame damage"]},
    "U0100": {"desc": "Lost Communication With ECM/PCM", "system": "network", "severity": "high",
              "causes": ["CAN bus wiring issue", "Faulty ECM/PCM", "Ground connection problem", "Low battery voltage"],
              "fixes": ["Check CAN bus wiring", "Test battery voltage", "Check ground connections", "Scan all modules"]},
    "U0101": {"desc": "Lost Communication With TCM", "system": "network", "severity": "high",
              "causes": ["CAN bus issue", "Faulty TCM", "Wiring damage"],
              "fixes": ["Check CAN bus wiring to TCM", "Test TCM power and ground", "Replace TCM if faulty"]},
}

# DTC prefix meanings
DTC_PREFIXES = {
    "P": "Powertrain", "C": "Chassis", "B": "Body", "U": "Network/Communication"
}

DTC_DIGIT2 = {
    "P": {"0": "Generic (SAE)", "1": "Manufacturer-specific", "2": "Generic (SAE)", "3": "Generic/Manufacturer"},
    "C": {"0": "Generic (SAE)", "1": "Manufacturer-specific", "2": "Manufacturer-specific", "3": "Generic (SAE)"},
    "B": {"0": "Generic (SAE)", "1": "Manufacturer-specific", "2": "Manufacturer-specific", "3": "Generic (SAE)"},
    "U": {"0": "Generic (SAE)", "1": "Manufacturer-specific", "2": "Manufacturer-specific", "3": "Generic (SAE)"},
}

DTC_SYSTEM_MAP = {
    "P0": {
        "1": "Fuel and Air Metering", "2": "Fuel and Air Metering (Injector)",
        "3": "Ignition System / Misfire", "4": "Auxiliary Emissions Controls",
        "5": "Vehicle Speed / Idle Control", "6": "Computer Output Circuit",
        "7": "Transmission", "8": "Transmission",
    },
    "P1": {"all": "Manufacturer-Specific Powertrain"},
    "C0": {"all": "Generic Chassis"},
    "B0": {"all": "Generic Body"},
    "U0": {"all": "Generic Network"},
}


def decode_dtc_format(code: str) -> dict:
    """Decode DTC code format to explain what each character means."""
    code = code.upper().strip()
    if not re.match(r'^[PCBU]\d{4}$', code):
        return {"error": f"Invalid DTC format: {code}. Expected format: P0300, C0035, B0100, U0100"}

    prefix = code[0]
    digit2 = code[1]
    digit3 = code[2]

    info = {
        "code": code,
        "category": DTC_PREFIXES.get(prefix, "Unknown"),
        "type": DTC_DIGIT2.get(prefix, {}).get(digit2, "Unknown"),
    }

    system_key = f"{prefix}{digit2}"
    if system_key in DTC_SYSTEM_MAP:
        sys_map = DTC_SYSTEM_MAP[system_key]
        info["subsystem"] = sys_map.get(digit3, sys_map.get("all", "Unknown"))
    else:
        info["subsystem"] = "Manufacturer-Specific"

    return info


def load_cache():
    """Load cached DTC data if available."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return None


def save_cache(data):
    """Save DTC data to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
    except IOError:
        pass


def fetch_dtc_database():
    """Fetch DTC database from GitHub. Returns dict of code->description."""
    cached = load_cache()
    if cached:
        return cached

    for name, url in DTC_URLS.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "VehicleDiagnostics/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                # Normalize to {code: description} format
                normalized = {}
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            code = item.get("code", item.get("dtc", ""))
                            desc = item.get("description", item.get("desc", item.get("meaning", "")))
                            if code and desc:
                                normalized[code.upper()] = desc
                elif isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, str):
                            normalized[k.upper()] = v
                        elif isinstance(v, dict):
                            normalized[k.upper()] = v.get("description", v.get("desc", str(v)))
                if normalized:
                    save_cache(normalized)
                    return normalized
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError):
            continue

    return None


def lookup_code(code: str) -> dict:
    """Look up a single DTC code. Returns structured result."""
    code = code.upper().strip()
    result = decode_dtc_format(code)
    if "error" in result:
        return result

    # Check built-in database first (has richer data)
    if code in COMMON_CODES:
        entry = COMMON_CODES[code]
        result.update({
            "description": entry["desc"],
            "severity": entry["severity"],
            "system": entry["system"],
            "common_causes": entry["causes"],
            "suggested_fixes": entry["fixes"],
            "source": "built-in"
        })
        return result

    # Try online database
    online_db = fetch_dtc_database()
    if online_db and code in online_db:
        result.update({
            "description": online_db[code],
            "source": "wal33d-database"
        })
        return result

    # No match found - still return format decode info
    result["description"] = "Code not found in database. Use web search for this code."
    result["source"] = "format-decode-only"
    return result


def search_codes(keyword: str) -> list:
    """Search codes by keyword in description."""
    keyword = keyword.lower()
    results = []

    # Search built-in codes
    for code, entry in COMMON_CODES.items():
        if keyword in entry["desc"].lower() or keyword in entry["system"].lower():
            results.append({"code": code, "description": entry["desc"], "system": entry["system"]})

    # Search online database
    online_db = fetch_dtc_database()
    if online_db:
        for code, desc in online_db.items():
            if keyword in desc.lower() and code not in [r["code"] for r in results]:
                results.append({"code": code, "description": desc})

    return results[:25]  # Limit results


def list_by_system(system: str) -> list:
    """List codes by vehicle system."""
    system = system.lower()
    system_aliases = {
        "engine": ["ignition", "fuel_air"],
        "trans": ["transmission"],
        "transmission": ["transmission"],
        "exhaust": ["emissions"],
        "emissions": ["emissions"],
        "brakes": ["abs"],
        "abs": ["abs"],
        "body": ["body"],
        "communication": ["network"],
        "network": ["network"],
        "cooling": ["cooling"],
    }
    target_systems = system_aliases.get(system, [system])

    results = []
    for code, entry in sorted(COMMON_CODES.items()):
        if entry["system"] in target_systems:
            results.append({"code": code, "description": entry["desc"], "severity": entry["severity"]})

    return results


def format_result(result: dict) -> str:
    """Format a lookup result for display."""
    lines = []
    if "error" in result:
        lines.append(f"ERROR: {result['error']}")
        return "\n".join(lines)

    lines.append(f"Code: {result['code']}")
    lines.append(f"Category: {result['category']}")
    lines.append(f"Type: {result['type']}")
    lines.append(f"Subsystem: {result.get('subsystem', 'N/A')}")
    lines.append(f"Description: {result.get('description', 'N/A')}")

    if "severity" in result:
        sev = result["severity"]
        sev_label = {"low": "LOW - Monitor", "moderate": "MODERATE - Address soon", "high": "HIGH - Address immediately"}.get(sev, sev)
        lines.append(f"Severity: {sev_label}")

    if "common_causes" in result:
        lines.append("Common Causes:")
        for cause in result["common_causes"]:
            lines.append(f"  - {cause}")

    if "suggested_fixes" in result:
        lines.append("Suggested Fixes:")
        for fix in result["suggested_fixes"]:
            lines.append(f"  - {fix}")

    lines.append(f"Source: {result.get('source', 'unknown')}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 dtc_lookup.py P0300           # Look up a code")
        print("  python3 dtc_lookup.py P0300 P0171     # Look up multiple codes")
        print("  python3 dtc_lookup.py --search misfire # Search by keyword")
        print("  python3 dtc_lookup.py --system engine  # List codes by system")
        print("  python3 dtc_lookup.py --json P0300     # Output as JSON")
        sys.exit(1)

    output_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    if args[0] == "--search" and len(args) > 1:
        keyword = " ".join(args[1:])
        results = search_codes(keyword)
        if output_json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Search results for '{keyword}' ({len(results)} found):\n")
            for r in results:
                print(f"  {r['code']}: {r['description']}")
            if not results:
                print("  No codes found. Try a different keyword.")

    elif args[0] == "--system" and len(args) > 1:
        system = args[1]
        results = list_by_system(system)
        if output_json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Codes for system '{system}' ({len(results)} found):\n")
            for r in results:
                print(f"  {r['code']}: {r['description']} [{r['severity']}]")
            if not results:
                print("  No codes found. Try: engine, transmission, emissions, brakes, body, network, cooling")

    else:
        # Look up one or more codes
        results = []
        for code in args:
            result = lookup_code(code)
            results.append(result)
            if not output_json:
                print(format_result(result))
                print("---")
        if output_json:
            print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

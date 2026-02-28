#!/usr/bin/env python3
"""
NHTSA Vehicle Safety Lookup Tool
Queries NHTSA APIs for VIN decoding, recalls, complaints, and investigations.

All APIs are free, no key required.

Usage:
  python3 nhtsa_lookup.py vin <VIN>                    # Decode VIN
  python3 nhtsa_lookup.py recalls <make> <model> <year> # Recalls by make/model/year
  python3 nhtsa_lookup.py recalls-vin <VIN>             # Recalls by VIN
  python3 nhtsa_lookup.py complaints <make> <model> <year> # Complaints
  python3 nhtsa_lookup.py investigations <make> <model> <year> # Investigations
  python3 nhtsa_lookup.py --json <any command>          # Output as JSON
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse

BASE_VPIC = "https://vpic.nhtsa.dot.gov/api/vehicles"
BASE_RECALLS = "https://api.nhtsa.gov/recalls/recallsByVehicle"
BASE_COMPLAINTS = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
BASE_RECALLS_VIN = "https://api.nhtsa.gov/recalls/recallsByVin"


def api_get(url: str) -> dict:
    """Make GET request to NHTSA API."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "VehicleDiagnostics/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        return {"error": str(e)}


def decode_vin(vin: str) -> dict:
    """Decode VIN using NHTSA vPIC API. Returns vehicle details."""
    url = f"{BASE_VPIC}/DecodeVinValuesExtended/{urllib.parse.quote(vin)}?format=json"
    data = api_get(url)

    if "error" in data:
        return data

    results = data.get("Results", [{}])
    if not results:
        return {"error": "No results returned"}

    raw = results[0]

    # Extract key fields (filter out empty values)
    vehicle = {}
    key_fields = [
        "Make", "Model", "ModelYear", "Trim", "BodyClass", "VehicleType",
        "DriveType", "FuelTypePrimary", "EngineCylinders", "EngineModel",
        "DisplacementL", "EngineHP", "TransmissionStyle", "TransmissionSpeeds",
        "PlantCity", "PlantState", "PlantCountry", "Manufacturer",
        "GVWR", "CurbWeightLB", "WheelBaseShort", "WheelBaseLong",
        "TrailerType", "TrailerBodyType", "TrailerLength",
        "BrakeSystemType", "ABS", "ESC", "TractionControl",
        "AirBagLocFront", "AirBagLocSide", "AirBagLocCurtain",
        "ForwardCollisionWarning", "LaneDepartureWarning", "AdaptiveCruiseControl",
        "BlindSpotMon", "RearCrossTrafficAlert", "ParkAssist",
        "TPMS", "KeylessIgnition", "AutoReverseSystem",
        "ErrorCode", "ErrorText", "AdditionalErrorText",
    ]

    for field in key_fields:
        val = raw.get(field, "")
        if val and str(val).strip() and str(val).strip() != "Not Applicable":
            vehicle[field] = str(val).strip()

    return vehicle


def get_recalls_by_vehicle(make: str, model: str, year: str) -> list:
    """Get recalls for a specific make/model/year."""
    params = urllib.parse.urlencode({"make": make, "model": model, "modelYear": year})
    url = f"{BASE_RECALLS}?{params}"
    data = api_get(url)

    if "error" in data:
        return [{"error": data["error"]}]

    results = data.get("results", [])
    recalls = []
    for r in results:
        recalls.append({
            "campaign": r.get("NHTSACampaignNumber", ""),
            "component": r.get("Component", ""),
            "summary": r.get("Summary", ""),
            "consequence": r.get("Consequence", ""),
            "remedy": r.get("Remedy", ""),
            "manufacturer": r.get("Manufacturer", ""),
            "report_date": r.get("ReportReceivedDate", ""),
        })

    return recalls


def get_recalls_by_vin(vin: str) -> list:
    """Get recalls for a specific VIN."""
    url = f"{BASE_RECALLS_VIN}?vin={urllib.parse.quote(vin)}"
    data = api_get(url)

    if "error" in data:
        return [{"error": data["error"]}]

    results = data.get("results", [])
    recalls = []
    for r in results:
        recalls.append({
            "campaign": r.get("NHTSACampaignNumber", ""),
            "component": r.get("Component", ""),
            "summary": r.get("Summary", ""),
            "consequence": r.get("Consequence", ""),
            "remedy": r.get("Remedy", ""),
        })

    return recalls


def get_complaints(make: str, model: str, year: str) -> list:
    """Get consumer complaints for a specific make/model/year."""
    params = urllib.parse.urlencode({"make": make, "model": model, "modelYear": year})
    url = f"{BASE_COMPLAINTS}?{params}"
    data = api_get(url)

    if "error" in data:
        return [{"error": data["error"]}]

    results = data.get("results", [])
    complaints = []
    for c in results:
        complaints.append({
            "component": c.get("components", ""),
            "summary": c.get("summary", ""),
            "crash": c.get("crash", "N"),
            "fire": c.get("fire", "N"),
            "injuries": c.get("injuries", 0),
            "date": c.get("dateComplaintFiled", ""),
            "odi_number": c.get("odiNumber", ""),
        })

    return complaints


def format_vin(vehicle: dict) -> str:
    """Format VIN decode results for display."""
    if "error" in vehicle:
        return f"Error: {vehicle['error']}"

    lines = ["=== VIN Decode Results ==="]
    basic = ["Make", "Model", "ModelYear", "Trim", "BodyClass", "VehicleType"]
    engine = ["FuelTypePrimary", "EngineCylinders", "EngineModel", "DisplacementL", "EngineHP"]
    trans = ["TransmissionStyle", "TransmissionSpeeds", "DriveType"]
    safety = ["ABS", "ESC", "TractionControl", "TPMS", "ForwardCollisionWarning",
              "LaneDepartureWarning", "BlindSpotMon", "AdaptiveCruiseControl"]

    for label, fields in [("Vehicle", basic), ("Engine", engine), ("Transmission", trans), ("Safety", safety)]:
        section_lines = []
        for f in fields:
            if f in vehicle:
                section_lines.append(f"  {f}: {vehicle[f]}")
        if section_lines:
            lines.append(f"\n{label}:")
            lines.extend(section_lines)

    if vehicle.get("ErrorCode") and vehicle["ErrorCode"] != "0":
        lines.append(f"\nWarning: {vehicle.get('ErrorText', 'Unknown error')}")
        if vehicle.get("AdditionalErrorText"):
            lines.append(f"  Detail: {vehicle['AdditionalErrorText']}")

    return "\n".join(lines)


def format_recalls(recalls: list) -> str:
    """Format recall results for display."""
    if not recalls:
        return "No recalls found."
    if recalls and "error" in recalls[0]:
        return f"Error: {recalls[0]['error']}"

    lines = [f"=== {len(recalls)} Recall(s) Found ==="]
    for i, r in enumerate(recalls, 1):
        lines.append(f"\n--- Recall {i} ---")
        lines.append(f"  Campaign: {r.get('campaign', 'N/A')}")
        lines.append(f"  Component: {r.get('component', 'N/A')}")
        lines.append(f"  Summary: {r.get('summary', 'N/A')}")
        lines.append(f"  Consequence: {r.get('consequence', 'N/A')}")
        lines.append(f"  Remedy: {r.get('remedy', 'N/A')}")
    return "\n".join(lines)


def format_complaints(complaints: list) -> str:
    """Format complaint results for display."""
    if not complaints:
        return "No complaints found."
    if complaints and "error" in complaints[0]:
        return f"Error: {complaints[0]['error']}"

    lines = [f"=== {len(complaints)} Complaint(s) Found ==="]
    # Group by component
    by_component = {}
    for c in complaints:
        comp = c.get("component", "Unknown")
        by_component.setdefault(comp, []).append(c)

    for comp, comp_complaints in sorted(by_component.items(), key=lambda x: -len(x[1])):
        lines.append(f"\n{comp} ({len(comp_complaints)} complaints):")
        for c in comp_complaints[:3]:  # Show top 3 per component
            summary = c.get("summary", "")[:200]
            crash_info = ""
            if c.get("crash") == "Y":
                crash_info = " [CRASH]"
            if c.get("fire") == "Y":
                crash_info += " [FIRE]"
            lines.append(f"  - {summary}{crash_info}")
        if len(comp_complaints) > 3:
            lines.append(f"  ... and {len(comp_complaints) - 3} more")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    output_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    command = args[0].lower()

    if command == "vin" and len(args) >= 2:
        vin = args[1]
        result = decode_vin(vin)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_vin(result))

    elif command == "recalls" and len(args) >= 4:
        make, model, year = args[1], args[2], args[3]
        result = get_recalls_by_vehicle(make, model, year)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_recalls(result))

    elif command == "recalls-vin" and len(args) >= 2:
        vin = args[1]
        result = get_recalls_by_vin(vin)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_recalls(result))

    elif command == "complaints" and len(args) >= 4:
        make, model, year = args[1], args[2], args[3]
        result = get_complaints(make, model, year)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_complaints(result))

    else:
        print("Invalid command. Use: vin, recalls, recalls-vin, complaints")
        print("Run without arguments for usage examples.")
        sys.exit(1)


if __name__ == "__main__":
    main()

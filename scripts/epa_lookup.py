#!/usr/bin/env python3
"""
EPA Fuel Economy Vehicle Specs Lookup
Queries the EPA/DOE fueleconomy.gov API for vehicle specifications and MPG data.

Free API, no key required.

Usage:
  python3 epa_lookup.py search <year> <make>           # List models for year/make
  python3 epa_lookup.py specs <vehicle_id>              # Get specs for specific vehicle
  python3 epa_lookup.py compare <id1> <id2>             # Compare two vehicles
  python3 epa_lookup.py makes <year>                    # List makes for a year
  python3 epa_lookup.py --json <any command>            # Output as JSON
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET

BASE_URL = "https://www.fueleconomy.gov/ws/rest"


def api_get(url: str, accept_json: bool = False) -> dict | list | None:
    """Make GET request to EPA API. Returns parsed response."""
    headers = {"User-Agent": "VehicleDiagnostics/1.0"}
    if accept_json:
        headers["Accept"] = "application/json"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode()
            content_type = resp.headers.get("Content-Type", "")

            if "json" in content_type or accept_json:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    pass

            # Parse XML response
            try:
                root = ET.fromstring(content)
                return xml_to_dict(root)
            except ET.ParseError:
                return {"raw": content}

    except (urllib.error.URLError, TimeoutError) as e:
        return {"error": str(e)}


def xml_to_dict(element) -> dict | list:
    """Convert XML element to dict."""
    if len(element) == 0:
        return element.text or ""

    result = {}
    children_tags = [child.tag for child in element]

    # If all children have the same tag, it's a list
    if len(set(children_tags)) == 1 and len(children_tags) > 1:
        return [xml_to_dict(child) for child in element]

    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data

    return result


def get_makes(year: str) -> list:
    """Get all vehicle makes for a given year."""
    url = f"{BASE_URL}/vehicle/menu/make?year={year}"
    data = api_get(url)

    if isinstance(data, dict) and "error" in data:
        return [data]

    if isinstance(data, list):
        return [{"make": item.get("text", item.get("value", "")) if isinstance(item, dict) else str(item)} for item in data]
    elif isinstance(data, dict):
        items = data.get("menuItem", [])
        if isinstance(items, dict):
            items = [items]
        if isinstance(items, list):
            return [{"make": item.get("text", "") if isinstance(item, dict) else str(item)} for item in items]

    return []


def search_vehicles(year: str, make: str) -> list:
    """Search for vehicles by year and make. Returns list of models with IDs."""
    url = f"{BASE_URL}/vehicle/menu/model?year={year}&make={urllib.parse.quote(make)}"
    data = api_get(url)

    if isinstance(data, dict) and "error" in data:
        return [data]

    models = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                models.append({"model": item.get("text", ""), "value": item.get("value", "")})
    elif isinstance(data, dict):
        items = data.get("menuItem", [])
        if isinstance(items, dict):
            items = [items]
        for item in items:
            if isinstance(item, dict):
                models.append({"model": item.get("text", ""), "value": item.get("value", "")})

    # For each model, get the vehicle options/IDs
    results = []
    for m in models:
        model_name = m.get("model", "")
        options_url = f"{BASE_URL}/vehicle/menu/options?year={year}&make={urllib.parse.quote(make)}&model={urllib.parse.quote(model_name)}"
        options_data = api_get(options_url)

        if isinstance(options_data, dict):
            items = options_data.get("menuItem", [])
            if isinstance(items, dict):
                items = [items]
            for item in items:
                if isinstance(item, dict):
                    results.append({
                        "model": model_name,
                        "variant": item.get("text", ""),
                        "id": item.get("value", ""),
                    })
        if not results:
            results.append({"model": model_name, "variant": "", "id": ""})

    return results if results else models


def get_vehicle_specs(vehicle_id: str) -> dict:
    """Get detailed specs for a specific vehicle ID."""
    url = f"{BASE_URL}/vehicle/{vehicle_id}"
    data = api_get(url)

    if isinstance(data, dict) and "error" in data:
        return data

    if isinstance(data, dict):
        # Extract key specs
        specs = {}
        field_map = {
            "make": "Make", "model": "Model", "year": "Year",
            "VClass": "Vehicle Class", "drive": "Drive Type",
            "trany": "Transmission", "displ": "Engine Displacement (L)",
            "cylinders": "Cylinders", "fuelType": "Fuel Type", "fuelType1": "Primary Fuel",
            "city08": "City MPG", "highway08": "Highway MPG", "comb08": "Combined MPG",
            "cityA08": "City MPG (Alt Fuel)", "highwayA08": "Highway MPG (Alt Fuel)",
            "co2TailpipeGpm": "CO2 (g/mi)", "fuelCost08": "Annual Fuel Cost ($)",
            "youSaveSpend": "You Save/Spend vs Average ($)",
            "ghgScore": "GHG Score (1-10)", "feScore": "Fuel Economy Score (1-10)",
            "atvType": "Alternative Fuel Type", "evMotor": "EV Motor",
            "rangeA": "EV Range (mi)", "charge120": "Charge Time 120V (hrs)",
            "charge240": "Charge Time 240V (hrs)", "phevBlended": "PHEV Blended",
            "startStop": "Start-Stop Technology", "tCharger": "Turbo/Supercharged",
        }

        for key, label in field_map.items():
            val = data.get(key, "")
            if val and str(val).strip() and str(val) != "0" and str(val) != "-1":
                specs[label] = str(val).strip()

        return specs

    return {"error": "Unexpected response format"}


def format_makes(makes: list) -> str:
    """Format makes list for display."""
    if not makes:
        return "No makes found for that year."
    lines = ["Available Makes:"]
    for m in makes:
        if isinstance(m, dict) and "error" in m:
            return f"Error: {m['error']}"
        make = m.get("make", str(m)) if isinstance(m, dict) else str(m)
        lines.append(f"  {make}")
    return "\n".join(lines)


def format_search(results: list, year: str, make: str) -> str:
    """Format search results for display."""
    if not results:
        return f"No vehicles found for {year} {make}."
    if results and isinstance(results[0], dict) and "error" in results[0]:
        return f"Error: {results[0]['error']}"

    lines = [f"=== {year} {make} Models ==="]
    for r in results:
        if isinstance(r, dict):
            model = r.get("model", "")
            variant = r.get("variant", "")
            vid = r.get("id", "")
            if vid:
                lines.append(f"  ID {vid}: {model} {variant}".strip())
            else:
                lines.append(f"  {model} {variant}".strip())
    lines.append("\nUse 'epa_lookup.py specs <ID>' for detailed specs.")
    return "\n".join(lines)


def format_specs(specs: dict) -> str:
    """Format vehicle specs for display."""
    if "error" in specs:
        return f"Error: {specs['error']}"

    lines = ["=== Vehicle Specifications ==="]
    categories = {
        "Vehicle": ["Make", "Model", "Year", "Vehicle Class", "Drive Type", "Transmission"],
        "Engine": ["Engine Displacement (L)", "Cylinders", "Fuel Type", "Primary Fuel", "Turbo/Supercharged"],
        "Fuel Economy": ["City MPG", "Highway MPG", "Combined MPG", "City MPG (Alt Fuel)", "Highway MPG (Alt Fuel)"],
        "Costs & Emissions": ["Annual Fuel Cost ($)", "You Save/Spend vs Average ($)", "CO2 (g/mi)", "GHG Score (1-10)", "Fuel Economy Score (1-10)"],
        "Electric/Hybrid": ["EV Motor", "EV Range (mi)", "Charge Time 120V (hrs)", "Charge Time 240V (hrs)", "Alternative Fuel Type", "PHEV Blended", "Start-Stop Technology"],
    }

    for cat, fields in categories.items():
        cat_lines = []
        for f in fields:
            if f in specs:
                cat_lines.append(f"  {f}: {specs[f]}")
        if cat_lines:
            lines.append(f"\n{cat}:")
            lines.extend(cat_lines)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    output_json = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--json"]

    command = args[0].lower()

    if command == "makes" and len(args) >= 2:
        year = args[1]
        result = get_makes(year)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_makes(result))

    elif command == "search" and len(args) >= 3:
        year = args[1]
        make = " ".join(args[2:])
        result = search_vehicles(year, make)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_search(result, year, make))

    elif command == "specs" and len(args) >= 2:
        vehicle_id = args[1]
        result = get_vehicle_specs(vehicle_id)
        if output_json:
            print(json.dumps(result, indent=2))
        else:
            print(format_specs(result))

    elif command == "compare" and len(args) >= 3:
        specs1 = get_vehicle_specs(args[1])
        specs2 = get_vehicle_specs(args[2])
        if output_json:
            print(json.dumps({"vehicle_1": specs1, "vehicle_2": specs2}, indent=2))
        else:
            print("=== Vehicle 1 ===")
            print(format_specs(specs1))
            print("\n=== Vehicle 2 ===")
            print(format_specs(specs2))

    else:
        print("Invalid command. Use: makes, search, specs, compare")
        sys.exit(1)


if __name__ == "__main__":
    main()

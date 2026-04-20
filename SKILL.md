---
name: vehicle-diagnostics
description: >
  Use when diagnosing vehicle problems from symptoms or DTC codes, checking recalls or NHTSA complaints,
  decoding a VIN, interpreting OBD-II data, researching known issues for a specific vehicle, looking up
  repair procedures, torque specs, or fluid specs, or providing step-by-step repair guidance for cars,
  trucks, motorcycles, RVs, boats, ATVs, and dirt bikes.
---

# Vehicle Diagnostics Skill

Diagnose vehicle problems and provide repair guidance using integrated tools, databases, and reference knowledge.

## Skill Directory

Personal Codex installs typically live under `~/.codex/skills/vehicle-diagnostics/`.

## Available Tools

### Scripts (run via bash)
| Script | Purpose | Usage |
|---|---|---|
| `scripts/dtc_lookup.py` | DTC code lookup (28,000+ codes) | `python3 <skill>/scripts/dtc_lookup.py P0300` |
| `scripts/nhtsa_lookup.py` | VIN decode, recalls, complaints, investigations, TSBs | `python3 <skill>/scripts/nhtsa_lookup.py vin <VIN>` |
| `scripts/epa_lookup.py` | EPA vehicle specs & MPG data | `python3 <skill>/scripts/epa_lookup.py search <year> <make>` |

### Reference Files (read when needed)
| File | When to Read |
|---|---|
| `references/diagnostic-trees.md` | Symptom-based troubleshooting (noises, won't start, overheating, vibration, brakes, transmission, electrical, leaks, AC, steering, suspension) |
| `references/torque-specs.md` | Vehicle-specific torque lookup workflow, source priority, search patterns, and response template |
| `references/fluid-specs.md` | Vehicle-specific fluid lookup workflow, source priority, search patterns, and response template |
| `references/common-repairs.md` | Step-by-step procedures: brakes, spark plugs, belts, battery, filters, thermostat, bearings, O2 sensors, alternator, starter, coolant flush, trans fluid, CV axle, tie rods, MAF cleaning, throttle body |
| `references/obd2-guide.md` | OBD-II PIDs, normal sensor ranges, fuel trim interpretation, monitor readiness, freeze frame, ELM327/python-obd usage |

## Diagnostic Workflow

### 1. Gather Vehicle Info
Ask for: Year, Make, Model, Engine, Mileage. VIN is ideal (decode with `nhtsa_lookup.py`).

For torque and fluid lookups, do not proceed on partial vehicle info if the exact spec depends on engine, drivetrain, trim, transmission, or axle. Ask for the missing details first.

### 2. Identify the Problem Type

**DTC Code Present** -> Run `dtc_lookup.py` for code definition, causes, and fixes. Then check NHTSA complaints, investigations, and TSBs for the vehicle to see if it's a known issue.

**Symptom Only** -> Read `references/diagnostic-trees.md` for the matching symptom category. Walk through the decision tree with the user.

**"Is this a known issue?"** -> Run `nhtsa_lookup.py complaints <make> <model> <year>`, `nhtsa_lookup.py investigations <make> <model> <year>`, and `nhtsa_lookup.py tsbs <make> <model> <year>` to check NHTSA complaints, investigations, and technical service bulletins. Search web/Reddit for "<year> <make> <model> <symptom>" common problems.

### 3. Research the Issue

Run these as needed (in parallel when possible):

```bash
# DTC lookup
python3 <skill>/scripts/dtc_lookup.py P0300 P0171

# Check for recalls
python3 <skill>/scripts/nhtsa_lookup.py recalls <make> <model> <year>
python3 <skill>/scripts/nhtsa_lookup.py recalls-vin <VIN>

# Check NHTSA complaints
python3 <skill>/scripts/nhtsa_lookup.py complaints <make> <model> <year>

# Check NHTSA investigations
python3 <skill>/scripts/nhtsa_lookup.py investigations <make> <model> <year>

# Check NHTSA TSBs
python3 <skill>/scripts/nhtsa_lookup.py tsbs <make> <model> <year>
python3 <skill>/scripts/nhtsa_lookup.py tsbs <make> <model> <year> --keyword "oil consumption"
python3 <skill>/scripts/nhtsa_lookup.py tsbs <make> <model> <year> --component "ENGINE" --limit 5

# DTC search by keyword
python3 <skill>/scripts/dtc_lookup.py --search "misfire"
python3 <skill>/scripts/dtc_lookup.py --system transmission

# Vehicle specs
python3 <skill>/scripts/epa_lookup.py search <year> <make>
python3 <skill>/scripts/epa_lookup.py specs <vehicle_id>
```

For forum research, use web search to search:
- `<year> <make> <model> <symptom OR code> site:reddit.com/r/MechanicAdvice`
- `<year> <make> <model> <symptom OR code> forum`
- `<year> <make> <model> common problems`

### 4. Torque and Fluid Requests

Treat torque and fluid requests as vehicle-specific research tasks, not generic reference lookups.

#### Torque requests

1. Collect `year make model engine` and the exact fastener/component.
2. Read `references/torque-specs.md`.
3. Search for an OEM or service-manual-quality spec for that exact vehicle and component.
4. Return the exact value, units, applicability, and any torque-angle or one-time-use notes.
5. If exact fitment cannot be verified, say that clearly and do not substitute a generic range.

#### Fluid requests

1. Collect `year make model engine` plus the exact system and transmission/drivetrain details if relevant.
2. Read `references/fluid-specs.md`.
3. Search for an owner’s-manual, OEM, or service-manual-quality spec for that exact vehicle and system.
4. Return the exact fluid spec, approval, capacity, applicability, and any compatibility warnings.
5. If exact fitment cannot be verified, say that clearly and do not substitute a generic manufacturer habit or color guess.

### 5. Provide Diagnosis

Present findings structured as:
1. **What the code/symptom means** (plain language)
2. **Most likely causes** (ordered by probability)
3. **How to confirm** (specific tests to narrow it down)
4. **Known issues** (NHTSA complaints, investigations, TSBs, forum consensus if found)
5. **Repair procedure** (reference common-repairs.md or provide custom steps)
6. **Parts and specs needed** (use vehicle-specific torque/fluid lookup workflow when applicable)
7. **Estimated difficulty** (DIY vs shop recommendation)
8. **Cost estimate range** (DIY parts vs shop labor + parts)

### 6. Safety Warnings

Always flag when applicable:
- Brake work: "Test brakes at low speed in a safe area before normal driving"
- Fuel system: "Relieve fuel pressure before disconnecting fuel lines. No open flames"
- Electrical: "Disconnect battery negative terminal first for any electrical work"
- Airbag/SRS: "Disconnect battery and wait 10+ minutes before working near airbag components"
- Exhaust: "Never work under a vehicle supported only by a jack. Use jack stands"
- Cooling system: "Never open a hot radiator cap. Let engine cool completely"
- Hybrid/EV: "High-voltage systems require specialized training. Do not touch orange cables"

## Script Reference

### dtc_lookup.py
```
python3 scripts/dtc_lookup.py <CODE>              # Look up single code
python3 scripts/dtc_lookup.py <CODE1> <CODE2>     # Multiple codes
python3 scripts/dtc_lookup.py --search <keyword>  # Search by keyword
python3 scripts/dtc_lookup.py --system <system>   # List by system (engine, transmission, emissions, brakes, body, network, cooling)
python3 scripts/dtc_lookup.py --json <CODE>       # JSON output
```

### nhtsa_lookup.py
```
python3 scripts/nhtsa_lookup.py vin <VIN>                      # Decode VIN
python3 scripts/nhtsa_lookup.py recalls <make> <model> <year>  # Recalls by vehicle
python3 scripts/nhtsa_lookup.py recalls-vin <VIN>              # Recalls by VIN
python3 scripts/nhtsa_lookup.py complaints <make> <model> <year>  # NHTSA complaints
python3 scripts/nhtsa_lookup.py investigations <make> <model> <year>  # NHTSA investigations
python3 scripts/nhtsa_lookup.py tsbs <make> <model> <year>            # NHTSA TSBs
python3 scripts/nhtsa_lookup.py tsbs <make> <model> <year> --keyword "misfire" --component "ENGINE" --limit 5
python3 scripts/nhtsa_lookup.py --json <command> <args>        # JSON output
```

### epa_lookup.py
```
python3 scripts/epa_lookup.py makes <year>                    # List makes for year
python3 scripts/epa_lookup.py search <year> <make>            # Search models
python3 scripts/epa_lookup.py specs <vehicle_id>              # Vehicle specs
python3 scripts/epa_lookup.py compare <id1> <id2>             # Compare vehicles
python3 scripts/epa_lookup.py --json <command> <args>         # JSON output
```

## Vehicle-Specific Considerations

### Motorcycles / Powersports
- Chain maintenance: clean, lube, adjust every 500-1000 miles
- Valve adjustment intervals vary widely (check service manual)
- Carbureted bikes: jets, float height, sync
- Coolant vs air-cooled: different overheating diagnostics

### RVs
- Chassis vs coach: two separate electrical systems
- Generator diagnostics: hours-based maintenance
- Roof inspection critical (water intrusion)
- LP system leak testing (soap solution on fittings)
- Slide-out mechanism: hydraulic vs electric

### Boats / Marine
- Raw water vs freshwater cooling systems
- Winterization critical (freeze damage)
- Lower unit gear oil: check for water contamination (milky = water intrusion through seals)
- Impeller replacement: annual or per manufacturer schedule
- Fuel stabilizer required for storage

### Diesel Engines
- Glow plug system (no spark plugs)
- DEF (Diesel Exhaust Fluid) system issues
- DPF (Diesel Particulate Filter) regeneration
- Fuel system priming after filter change or running out of fuel
- Injector coding/programming may be required after replacement

### Electric / Hybrid Vehicles
- 12V auxiliary battery still exists and can fail
- Regenerative braking affects brake wear patterns
- High-voltage battery degradation diagnostics
- Inverter/charger fault codes are manufacturer-specific
- Coolant systems for battery packs (separate from cabin HVAC)

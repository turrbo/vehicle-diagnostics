---
name: vehicle-diagnostics
description: >
  Comprehensive vehicle diagnostic and repair advisor for all vehicle types (cars, trucks, motorcycles,
  RVs, boats, ATVs, dirt bikes). Diagnose problems from symptoms or DTC codes, look up repair procedures,
  search forums and NHTSA complaints for known issues, find recalls, decode VINs, and provide step-by-step
  repair guidance with torque specs and fluid specifications. Integrates with NHTSA APIs (free, no key),
  DTC code databases, EPA vehicle specs, and web/Reddit forum search. Use when the user asks to: diagnose
  a vehicle problem, look up a check engine light code, troubleshoot symptoms (noises, vibrations, leaks,
  overheating, won't start), find recalls or TSBs, look up repair procedures, check torque specs, find
  correct fluids, interpret OBD-II data, research known issues for a specific vehicle, or get step-by-step
  repair instructions. Complements the "mechanic" skill (maintenance tracking) by focusing on diagnosis
  and repair.
---

# Vehicle Diagnostics Skill

Diagnose vehicle problems and provide repair guidance using integrated tools, databases, and reference knowledge.

## Skill Directory

`~/.claude/skills/vehicle-diagnostics/`

## Available Tools

### Scripts (run via bash)
| Script | Purpose | Usage |
|---|---|---|
| `scripts/dtc_lookup.py` | DTC code lookup (28,000+ codes) | `python3 <skill>/scripts/dtc_lookup.py P0300` |
| `scripts/nhtsa_lookup.py` | VIN decode, recalls, complaints | `python3 <skill>/scripts/nhtsa_lookup.py vin <VIN>` |
| `scripts/epa_lookup.py` | EPA vehicle specs & MPG data | `python3 <skill>/scripts/epa_lookup.py search <year> <make>` |

### Reference Files (read when needed)
| File | When to Read |
|---|---|
| `references/diagnostic-trees.md` | Symptom-based troubleshooting (noises, won't start, overheating, vibration, brakes, transmission, electrical, leaks, AC, steering, suspension) |
| `references/torque-specs.md` | Lug nut torque, spark plugs, brake components, suspension, engine fasteners, general bolt torque by size |
| `references/fluid-specs.md` | Engine oil, transmission fluid, coolant, brake fluid, power steering, gear oil, grease types by manufacturer |
| `references/common-repairs.md` | Step-by-step procedures: brakes, spark plugs, belts, battery, filters, thermostat, bearings, O2 sensors, alternator, starter, coolant flush, trans fluid, CV axle, tie rods, MAF cleaning, throttle body |
| `references/obd2-guide.md` | OBD-II PIDs, normal sensor ranges, fuel trim interpretation, monitor readiness, freeze frame, ELM327/python-obd usage |

## Diagnostic Workflow

### 1. Gather Vehicle Info
Ask for: Year, Make, Model, Engine, Mileage. VIN is ideal (decode with nhtsa_lookup.py).

### 2. Identify the Problem Type

**DTC Code Present** -> Run `dtc_lookup.py` for code definition, causes, and fixes. Then search NHTSA complaints for the vehicle to see if it's a known issue.

**Symptom Only** -> Read `references/diagnostic-trees.md` for the matching symptom category. Walk through the decision tree with the user.

**"Is this a known issue?"** -> Run `nhtsa_lookup.py complaints <make> <model> <year>` to check NHTSA complaints database. Search web/Reddit for "<year> <make> <model> <symptom>" common problems.

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

# DTC search by keyword
python3 <skill>/scripts/dtc_lookup.py --search "misfire"
python3 <skill>/scripts/dtc_lookup.py --system transmission

# Vehicle specs
python3 <skill>/scripts/epa_lookup.py search <year> <make>
python3 <skill>/scripts/epa_lookup.py specs <vehicle_id>
```

For forum research, use the web-search skill to search:
- `<year> <make> <model> <symptom OR code> site:reddit.com/r/MechanicAdvice`
- `<year> <make> <model> <symptom OR code> forum`
- `<year> <make> <model> common problems`

### 4. Provide Diagnosis

Present findings structured as:
1. **What the code/symptom means** (plain language)
2. **Most likely causes** (ordered by probability)
3. **How to confirm** (specific tests to narrow it down)
4. **Known issues** (NHTSA complaints, forum consensus if found)
5. **Repair procedure** (reference common-repairs.md or provide custom steps)
6. **Parts and specs needed** (reference torque-specs.md and fluid-specs.md)
7. **Estimated difficulty** (DIY vs shop recommendation)
8. **Cost estimate range** (DIY parts vs shop labor + parts)

### 5. Safety Warnings

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

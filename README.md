# Vehicle Diagnostics Skill

Use when diagnosing vehicle problems from symptoms or DTC codes, checking recalls or NHTSA complaints, decoding a VIN, interpreting OBD-II data, researching known issues for a specific vehicle, looking up repair procedures, torque specs, or fluid specs, or providing step-by-step repair guidance for cars, trucks, motorcycles, RVs, boats, ATVs, and dirt bikes.

## What this repo contains

- `SKILL.md` — the primary agent skill definition and workflow.
- `references/` — supporting playbooks, platform rules, examples, or data used by the skill.
- `scripts/` — executable helper tools used by the skill.
- `data/` — local reference datasets used by the skill.
- `tests/` — validation tests for scripts or data.

## Helper scripts

- `scripts/dtc_lookup.py`
- `scripts/nhtsa_lookup.py`
- `scripts/epa_lookup.py`
- `scripts/ev_fault_lookup.py`

## Reference material

- `references/fluid-specs.md`
- `references/ev-safety-and-scope.md`
- `references/common-repairs.md`
- `references/torque-specs.md`
- `references/obd2-guide.md`
- `references/diagnostic-trees.md`
- `references/ev-diagnostic-trees.md`
- `references/ev-oem-playbooks.md`

## Installation

Copy this repository or the skill directory into your agent's skills directory, then load the skill by name when the task matches its use case.

```bash
# example
cp -R vehicle-diagnostics ~/.claude/skills/vehicle-diagnostics
```

## Repository layout

```text
data/
  ev_fault_families.json
references/
  common-repairs.md
  diagnostic-trees.md
  ev-diagnostic-trees.md
  ev-oem-playbooks.md
  ev-safety-and-scope.md
  fluid-specs.md
  obd2-guide.md
  torque-specs.md
scripts/
  dtc_lookup.py
  epa_lookup.py
  ev_fault_lookup.py
  nhtsa_lookup.py
tests/
SKILL.md
```

## Notes

The root README summarizes the live repository contents. The complete operational instructions remain in `SKILL.md`.

# Hybrid / EV OEM Playbooks

Use these pattern-based notes after routing into the EV trees or when `scripts/ev_fault_lookup.py` returns a matching family. These are intentionally curated and non-exhaustive.

## Toyota / Lexus Hybrids

### HV Battery Deterioration (`P0A80`, `P0A7F`)
- Common pattern: warning lights, frequent engine cycling, rapid state-of-charge swings, poor EV assist
- First checks:
  - Verify 12V battery health
  - Inspect rear-seat or trunk battery cooling intake and fan path for blockage
  - Review block-voltage spread and battery temperature sensors with a hybrid-capable scan tool
- Escalate when:
  - Pack disassembly, module balancing, or internal resistance confirmation would be required

### Inverter Cooling / Overtemp (`P0A93`)
- Common pattern: red triangle, reduced power, intermittent no-ready, or shutdown after heat soak
- First checks:
  - Check inverter coolant level only when cold
  - Inspect for coolant turbulence/flow where the service design makes that externally visible
  - Check inverter coolant pump feed and related low-voltage protection devices
- Escalate when:
  - Internal inverter or converter diagnosis is needed

## Tesla

### Charge-Port / AC Charge Families (`CP_*`)
- Common pattern: charging starts then stops, latch errors, "check power source," or AC-only failures
- First checks:
  - Try a known-good EVSE
  - Inspect the charge port for debris, latch problems, or heat discoloration
  - Determine whether DC fast charging still works
- Escalate when:
  - The next step requires charge-port removal, onboard charger testing, or service-mode procedures beyond safe external checks

### Battery / Isolation / Thermal Families (`BMS_*`)
- Common pattern: isolation alerts, battery temp alerts, reduced power, or charging blocked due to pack protection
- First checks:
  - Confirm 12V support voltage is stable
  - Review alert history, temperature context, and whether the issue follows rain, washing, flooding, or collision damage
  - Check for visible coolant loss or external damage history
- Escalate when:
  - The vehicle reports persistent isolation or pack-internal faults

## GM Ultium / Volt / Bolt

### Isolation / Pack Protection (`P0AA6`, related BECM families)
- Common pattern: propulsion disabled, service high-voltage system, charging disabled, or no-ready complaints
- First checks:
  - Start with 12V battery condition
  - Look for coolant leak history, collision work, or water intrusion
  - Scan all modules for matching thermal, charger, and battery controller faults
- Escalate when:
  - Insulation testing or HV connector separation would be required

### Charge Enable / Battery Controller Families
- Common pattern: AC or DC charging blocked, reduced propulsion, or intermittent charge-stop complaints
- First checks:
  - Separate AC-only from DC-only failures
  - Review battery temperature and coolant-pump behavior
  - Check for software campaigns or OEM service bulletins before assuming hardware failure

## Hyundai / Kia E-GMP

### ICCU / DC-DC / Charge Families
- Common pattern: 12V battery warnings, charging interruption, no-start/no-ready after low-voltage events
- First checks:
  - Verify 12V battery condition before deeper HV diagnosis
  - Determine whether the fault affects AC charging, DC charging, or both
  - Inspect charge-port condition and low-voltage protections
- Escalate when:
  - ICCU or onboard charger confirmation requires HV component access or energized measurements

### Battery / Inverter Thermal Families
- Common pattern: repeated fast-charge slowdown, reduced power after highway use, battery conditioning complaints
- First checks:
  - Review battery/inverter temperatures and coolant-pump behavior
  - Check for recent coolant service or evidence of trapped air / low coolant
  - Compare cabin HVAC behavior with battery conditioning complaints

## Nissan Leaf

### Battery Temperature / Rapid-Charge Limits
- Common pattern: first fast charge is normal, later sessions slow dramatically, or battery temp bars stay elevated
- First checks:
  - Clarify whether the complaint appears after repeated DC fast charges
  - Review battery temperature data or dash temperature indication
  - Separate normal heat protection from a persistent temperature-sensor fault

### Onboard Charger / DC-DC Support
- Common pattern: AC charging refusal, weak 12V battery, or intermittent no-ready tied to low-voltage support issues
- First checks:
  - Verify 12V battery health
  - Test with a known-good EVSE
  - Inspect charge-port condition and low-voltage fuses
- Escalate when:
  - Charger or DC-DC diagnosis would require HV component access

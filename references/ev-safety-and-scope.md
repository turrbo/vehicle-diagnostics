# Hybrid / EV Safety and Scope

This skill supports triage, plain-language interpretation, and low-risk external checks for electrified vehicles. It is **not** a replacement for OEM service information or high-voltage training.

## Safe Guidance This Skill May Provide
- 12V battery and low-voltage power checks
- Reading and interpreting DTCs, freeze-frame, and live data
- External cooling-airflow inspections
- Coolant level and visible leak checks when the system is cold and safe to inspect
- Charge-port inspection for debris, latch issues, or obvious damage
- Fuse, relay, and accessible low-voltage connector inspection
- OEM playbook routing based on code family and symptom pattern

## Never Instruct The User To
- Touch orange cables or disconnect high-voltage connectors
- Probe HV circuits with a multimeter or megger
- Open a battery pack, inverter, onboard charger, or heater assembly
- Bypass interlocks, relays, contactors, or charge-port safety devices
- Perform refrigerant or coolant-loop service that requires OEM bleed/fill procedures without the correct service information and tools

## Mandatory Escalation Triggers
- Isolation faults or any fault that suggests possible loss of HV insulation
- Pack-internal contactor, cell, sensor, or internal communication faults
- Any diagnosis that would require energized measurements on HV circuits
- Any recommendation that would require pack opening or internal module replacement
- Coolant intrusion, collision damage, rodent damage, or flood exposure involving HV components

## Communication Pattern
When the skill hits one of the escalation triggers above, the response should:
1. Explain the fault in plain language
2. Identify the highest-value low-risk confirmation step already completed or still safe to do
3. State clearly that the next step requires HV-trained service
4. Avoid offering workaround steps that defeat safety interlocks

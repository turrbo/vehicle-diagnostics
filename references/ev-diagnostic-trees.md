# Hybrid / EV Diagnostic Trees

Structured troubleshooting flows for electrified vehicles. Use these before generic ICE-oriented trees when the vehicle is a hybrid, plug-in hybrid, or battery EV, or when the complaint involves charging, high-voltage propulsion, or battery thermal control.

## Table of Contents
- [HV Battery Faults](#hv-battery-faults)
- [Inverter / Drive Unit Faults](#inverter--drive-unit-faults)
- [Charge Faults](#charge-faults)
- [Thermal System Faults](#thermal-system-faults)

---

## HV Battery Faults

### Reduced Power / Battery Performance / No-Ready State
1. **Confirm safe state first**
   - Vehicle will not enter READY, shows stop safely / propulsion reduced, or has hybrid battery warning -> Continue
   - Vehicle only has a generic 12V low-voltage complaint -> Start with 12V battery and charging-system checks
2. **Check 12V support health**
   - Low or unstable 12V battery voltage -> Correct 12V problem first, clear codes, then re-evaluate
   - 12V system healthy -> Step 3
3. **Read all module DTCs**
   - Isolation / contactor / battery deterioration / cell imbalance families present -> Step 4
   - Only network or communication codes -> Check low-voltage power, grounds, and module wake-up issues first
4. **Review battery live data**
   - Large block-voltage spread, rapid SOC swings, or repeated battery temp spikes -> Suspect battery aging or cooling issue
   - Normal voltages but persistent contactor or isolation faults -> Escalate to HV-trained service
5. **Inspect low-risk external items**
   - Battery cooling intake blocked, fan noisy, pet hair/dust buildup, recent water intrusion -> Correct external issue and retest
   - No external fault found -> Escalate if pack opening or insulation testing would be required

### Isolation / Contactor / Pack Communication Faults
1. **Do not touch orange cables or separate HV connectors**
2. **Check history**
   - Collision, flood, coolant leak, rodent damage, or recent service -> Raises likelihood of isolation or connector sealing issue
3. **Check companion faults**
   - Thermal or charger faults alongside isolation faults -> Follow those trees too; they often point to the failed subsystem
4. **Escalate**
   - Any next step requiring insulation resistance testing, pack opening, or energized HV measurement is outside DIY scope

---

## Inverter / Drive Unit Faults

### No-Ready / Propulsion Disabled / Motor Shutdown
1. **Confirm complaint**
   - No READY state, sudden stop, no drive engagement, or repeated propulsion shutdown -> Continue
2. **Check 12V battery and low-voltage supply**
   - Weak 12V can mimic inverter or contactor faults -> Correct first
   - 12V stable -> Step 3
3. **Read DTC families and freeze-frame**
   - Inverter overcurrent / resolver / current-sensor / inverter-performance families present -> Step 4
   - Only charger or battery temperature faults -> Follow charge or thermal tree first
4. **Check external support systems**
   - Inverter coolant low, no circulation, pump fuse open, or obvious leak -> Address low-risk external issue and retest
   - No external issue -> Escalate
5. **Escalate**
   - Inverter internal faults, motor resolver faults, or drive-unit current-sensor faults generally require OEM service information and HV-safe tooling

### DC-DC Related Symptoms
1. **Look for 12V warning messages, repeated jump-start need, or low-voltage module resets**
2. **Verify whether the vehicle charges the 12V battery while in READY**
   - No -> Suspect DC-DC / integrated power electronics support issue
   - Yes -> Continue with normal parasitic draw or 12V battery testing
3. **If EV/hybrid DTCs point to ICCU, onboard charger, or inverter/DC-DC families**
   - Use OEM playbook and escalate before any HV disassembly

---

## Charge Faults

### AC Charge Refusal / Intermittent Charge Stops
1. **Clarify the failure mode**
   - AC-only fault -> Focus on charge port, pilot/proximity, onboard charger, and EVSE compatibility
   - DC-only fault -> Focus on pack temperature, fast-charge permissions, contactor/thermal restrictions, and DC charge communication
   - Both AC and DC fail -> Suspect broader battery, contactor, or low-voltage support problem
2. **Rule out external equipment first**
   - Try a known-good EVSE or charger if available
   - Same failure everywhere -> Step 3
3. **Inspect low-risk external items**
   - Charge-port debris, latch issue, heat damage, bent pins, water intrusion, low-voltage fuse issue
4. **Check battery temperature and charge-state conditions**
   - Pack too cold or too hot -> Charging may be intentionally limited; follow thermal tree
   - Temperatures normal -> Step 5
5. **Read DTC families**
   - Pilot/proximity / onboard charger / charge-enable families present -> Use OEM playbook
   - No useful DTCs and fault is repeatable -> Escalate for OEM diagnostics

### DC Fast-Charge Refusal
1. **Confirm whether AC charging still works**
   - Yes -> Often thermal, software, or DC handshake related
   - No -> Look for broader charger or battery enable fault
2. **Check pack temperature and recent drive/charge history**
   - Multiple recent fast-charge sessions or hot-soak condition -> Thermal derate likely
3. **Check for software campaigns / known OEM updates**
   - If known charge-control campaigns exist, recommend OEM check before part replacement

---

## Thermal System Faults

### Battery / Inverter Overtemp / Slow Charge Due to Temperature
1. **Confirm which subsystem is hot**
   - Battery temp warning, charge slows, fast charging blocked -> Battery thermal path
   - Propulsion derate with inverter temp or pump codes -> Inverter thermal path
2. **Check coolant level and obvious leaks only when safe and cold**
   - Low coolant / visible leak -> Correct external issue and retest
   - Level normal -> Step 3
3. **Check coolant flow / support hardware**
   - Pump inoperative, cooling fan issue, clogged battery intake, valve/chiller not responding -> Suspect thermal support component
4. **Check HVAC interaction**
   - Battery conditioning complaints that coincide with weak cabin A/C or heater performance can point to shared chiller/HVAC problems
5. **Escalate**
   - If the next step requires refrigerant work, battery chiller diagnosis, inverter disassembly, or pack service, stop and escalate

### Cold-Soak Charging Limits
1. **Confirm ambient conditions and preconditioning status**
2. **Differentiate normal limitation from fault**
   - Predictable charging slowdown in cold weather with no DTCs -> Often normal protection behavior
   - Charging blocked or persistent temp-sensor DTCs -> Follow OEM playbook and escalate as needed

# OBD-II Diagnostics Guide

Reference for interpreting OBD-II data, sensor readings, and diagnostic procedures.

## Table of Contents
- [OBD-II Basics](#obd-ii-basics)
- [Connector Location](#connector-location)
- [Live Data PIDs - Normal Ranges](#live-data-pids---normal-ranges)
- [Monitor Readiness](#monitor-readiness)
- [Freeze Frame Data](#freeze-frame-data)
- [Mode Descriptions](#mode-descriptions)
- [Common Diagnostic Procedures](#common-diagnostic-procedures)
- [ELM327 Adapter Usage](#elm327-adapter-usage)

---

## OBD-II Basics

OBD-II (On-Board Diagnostics II) is standardized on all US vehicles since 1996. It provides access to:
- Diagnostic Trouble Codes (DTCs)
- Live sensor data (PIDs)
- Freeze frame data (snapshot when code set)
- Emissions readiness monitors
- Vehicle information (VIN, calibration IDs)

### Code Format
- **P** = Powertrain, **C** = Chassis, **B** = Body, **U** = Network
- Second digit: **0** = Generic (SAE), **1** = Manufacturer-specific
- Third digit: Subsystem (1=fuel/air, 3=ignition, 4=emissions, 5=speed/idle, 7=transmission)
- Last two digits: Specific fault

---

## Connector Location

The OBD-II port is a 16-pin trapezoidal connector, always within 3 feet of the driver, accessible without tools.

**Common locations:**
- Under dashboard, left of steering column (most common)
- Under dashboard, right of steering column
- Behind ash tray or center console panel
- Under dashboard center, above pedals
- Inside center console compartment

---

## Live Data PIDs - Normal Ranges

### Engine Data
| PID | Description | Normal Range | Abnormal Indicates |
|---|---|---|---|
| RPM | Engine speed | 600-900 idle, per load | Erratic idle = ISC, vacuum leak |
| ECT | Engine coolant temp | 195-220F operating | High = cooling issue, Low = thermostat |
| IAT | Intake air temp | Ambient to +20F | Significantly above ambient = heat soak |
| MAP | Manifold absolute pressure | 15-22 inHg idle, near 0 at WOT | High at idle = vacuum leak |
| MAF | Mass air flow | 2-7 g/s idle (4-cyl), varies with engine | Low = dirty MAF, High = leak after MAF |
| TPS | Throttle position | 0-2% closed, 95-100% WOT | Erratic signal = bad TPS |
| STFT | Short term fuel trim | -10% to +10% | >+15% = lean condition, <-15% = rich |
| LTFT | Long term fuel trim | -10% to +10% | >+15% = lean condition, <-15% = rich |
| O2S B1S1 | Upstream O2 sensor | Oscillates 0.1-0.9V rapidly | Stuck lean or rich = bad sensor or fuel issue |
| O2S B1S2 | Downstream O2 sensor | Steady 0.4-0.6V | Oscillates like upstream = bad catalytic converter |
| Spark Adv | Ignition timing | 10-35 degrees BTDC | Excessive retard = knock detected |
| Fuel Press | Fuel rail pressure | 35-65 PSI (port inj), 500-2500 PSI (DI) | Low = pump/filter/regulator issue |
| EVAP Purge | EVAP purge duty | 0% at idle cold, varies | Stuck = EVAP codes |
| EGR | EGR valve position | 0% at idle, opens at cruise | Stuck open = rough idle, closed = P0401 |

### Fuel Trim Interpretation
Fuel trims are the most useful diagnostic PID. They show how much the ECU is adjusting fuel delivery.

| STFT + LTFT Combined | Interpretation | Common Causes |
|---|---|---|
| +10% to +25% | Mild lean | Slight vacuum leak, dirty MAF, marginal fuel pressure |
| +25% or higher | Severe lean | Major vacuum leak, fuel pump weak, MAF failed |
| -10% to -25% | Mild rich | Leaking injector, high fuel pressure, dirty air filter |
| -25% or lower | Severe rich | Stuck-open injector, bad FPR, saturated charcoal canister |
| Bank 1 lean, Bank 2 normal | Unilateral lean | Vacuum leak on bank 1 side, injector issue bank 1 |
| Both banks equally lean | Bilateral lean | MAF, fuel pressure, large vacuum leak |

**Technique**: At idle, spray carb cleaner around intake components. If fuel trims drop when spraying a location, you found the vacuum leak.

### Transmission Data
| PID | Description | Normal Range |
|---|---|---|
| Trans Temp | Transmission fluid temperature | 175-220F normal, >250F = overheating |
| TCC | Torque converter clutch | Locked in highway cruise, unlocked at stop |
| Gear Ratio | Calculated gear | Should match expected ratios for vehicle |
| Shift Time | Time to complete shift | <0.5 sec normal |
| Line Pressure | Transmission line pressure | Varies by gear and load |

### Other Key Data
| PID | Description | Normal Range |
|---|---|---|
| Battery Volt | System voltage | 13.5-14.5V running, 12.4V+ key on |
| Catalyst Temp | Catalytic converter temp | 500-1200F normal operation |
| Misfire Count | Misfire events per cylinder | 0 at idle, occasional at high load OK |
| Knock Retard | Knock-related timing retard | 0 degrees ideal, <5 degrees acceptable |

---

## Monitor Readiness

OBD-II runs self-tests called "monitors." All monitors must be "ready" (completed) for emissions testing.

### Continuous Monitors (always running)
- **Misfire** - Detects misfires in real time
- **Fuel System** - Monitors fuel trim adjustments
- **Comprehensive Component** - Checks sensor rationality

### Non-Continuous Monitors (run under specific conditions)
| Monitor | Drive Conditions Required |
|---|---|
| Catalyst | Steady cruise 40-65 mph for 2-5 min |
| EVAP | Cold start, specific temp range, steady driving |
| Oxygen Sensor | Mixed driving, accel/decel cycles |
| O2 Heater | Cold start, idle until warm |
| EGR | Decel from highway speed, steady cruise |
| Secondary Air | Cold start (if equipped) |

### How to Complete Drive Cycle
1. Cold start (engine at ambient temp, 8+ hours sitting)
2. Idle 2 minutes
3. Accelerate moderately to 55 mph
4. Cruise at 55 mph for 3 minutes
5. Decelerate to 20 mph without braking (foot off gas)
6. Accelerate to 55-60 mph
7. Cruise at 55-60 mph for 5 minutes
8. Decelerate and stop. Idle for 2 minutes
9. Check readiness - most monitors should be complete

**Tip**: Some states allow 1-2 monitors "not ready" for emissions testing (varies by state and vehicle year).

---

## Freeze Frame Data

When a DTC sets, the ECU stores a snapshot of engine parameters at that moment. This data is invaluable for diagnosis.

### Key Freeze Frame Parameters
- **Engine RPM** - Was it at idle or under load?
- **Vehicle Speed** - Stationary, city, or highway?
- **Engine Load** - Light cruise or heavy acceleration?
- **Coolant Temp** - Cold start issue or warm running issue?
- **Fuel Trims** - What was the fuel system doing?
- **Intake Temp** - Any heat-related factors?

### How to Use Freeze Frame
1. Read freeze frame data for the stored code
2. Identify the driving conditions when the fault occurred
3. Try to recreate those exact conditions while monitoring live data
4. Watch the relevant PIDs approach the threshold that triggered the code

---

## Mode Descriptions

| Mode | Name | Description |
|---|---|---|
| 01 | Live Data | Current sensor readings (PIDs) |
| 02 | Freeze Frame | Snapshot data when code set |
| 03 | Stored DTCs | Confirmed trouble codes |
| 04 | Clear DTCs | Clear codes and reset monitors |
| 05 | O2 Sensor Test | O2 sensor monitoring results |
| 06 | On-Board Monitor | Component test results (thresholds and actual values) |
| 07 | Pending DTCs | Codes that have set once but not confirmed |
| 08 | Component Control | Bi-directional control (limited) |
| 09 | Vehicle Information | VIN, calibration IDs, CVNs |
| 0A | Permanent DTCs | Codes that can only be cleared by driving successfully |

### Mode 06 - The Most Underused Diagnostic Tool
Mode 06 shows the actual test results vs. pass/fail thresholds. This is incredibly useful:
- You can see if a component is TRENDING toward failure even before a code sets
- Example: Catalyst monitor shows actual efficiency at 0.08, threshold is 0.10. The cat is failing but hasn't tripped the code yet

---

## Common Diagnostic Procedures

### Parasitic Draw Test (Battery Drain)
1. Fully charge battery
2. Close all doors, ensure all lights off
3. Disconnect negative battery cable
4. Set multimeter to 10A or 20A DC
5. Connect multimeter in series (between cable and terminal)
6. Wait 30-60 min for modules to sleep
7. Switch to mA range
8. Normal draw: 20-50mA
9. If high: Pull fuses one at a time, note which circuit drops the draw
10. Investigate that circuit for stuck relay, aftermarket accessory, or module not sleeping

### Voltage Drop Test
Tests the quality of electrical connections under load.

**Ground side:**
1. Set multimeter to DC voltage (low range)
2. Connect one lead to engine block, other to battery negative terminal
3. Crank engine (or turn on high-draw accessory)
4. Should read <0.2V. Higher = bad ground connection

**Positive side:**
1. Connect one lead to alternator B+ terminal, other to battery positive
2. Engine running with loads on (headlights, blower)
3. Should read <0.3V. Higher = bad connection in charging circuit

### Relative Compression Test (with scan tool)
1. Disable fuel injectors and ignition
2. Monitor cranking RPM per cylinder
3. All cylinders should produce similar RPM peaks
4. A cylinder with noticeably lower RPM peak = low compression on that cylinder
5. Faster and less invasive than traditional compression test

---

## ELM327 Adapter Usage

The python-obd library enables reading OBD-II data through an ELM327 adapter.

### Setup
```
pip install obd
```

### Connection Types
| Type | Connection | Speed | Range |
|---|---|---|---|
| USB ELM327 | /dev/ttyUSB0 | Fast | Wired only |
| Bluetooth ELM327 | Pair first | Moderate | ~30 feet |
| WiFi ELM327 | 192.168.0.10:35000 | Moderate | ~30 feet |

### Basic Usage (python-obd)
```python
import obd

# Auto-connect
connection = obd.OBD()

# Read RPM
cmd = obd.commands.RPM
response = connection.query(cmd)
print(response.value)  # e.g., 850 revolutions_per_minute

# Read all available PIDs
for cmd in connection.supported_commands:
    response = connection.query(cmd)
    if response.value is not None:
        print(f"{cmd.name}: {response.value}")

# Read DTCs
dtcs = connection.query(obd.commands.GET_DTC)
print(dtcs.value)  # list of (code, description) tuples

# Clear DTCs (use with caution)
connection.query(obd.commands.CLEAR_DTC)
```

### Common PIDs for python-obd
| Command | PID | Returns |
|---|---|---|
| obd.commands.RPM | 010C | Engine RPM |
| obd.commands.SPEED | 010D | Vehicle speed |
| obd.commands.COOLANT_TEMP | 0105 | Coolant temperature |
| obd.commands.SHORT_FUEL_TRIM_1 | 0106 | Bank 1 STFT |
| obd.commands.LONG_FUEL_TRIM_1 | 0107 | Bank 1 LTFT |
| obd.commands.INTAKE_PRESSURE | 010B | MAP sensor |
| obd.commands.MAF | 0110 | Mass air flow |
| obd.commands.THROTTLE_POS | 0111 | Throttle position |
| obd.commands.O2_B1S1 | 0114 | O2 sensor B1S1 |
| obd.commands.GET_DTC | 03 | Stored DTCs |
| obd.commands.FREEZE_DTC | 02 | Freeze frame DTC |
| obd.commands.STATUS | 0101 | Monitor readiness |

### Async Monitoring
```python
import obd

connection = obd.Async()

# Watch RPM
connection.watch(obd.commands.RPM)
connection.watch(obd.commands.COOLANT_TEMP)
connection.watch(obd.commands.SHORT_FUEL_TRIM_1)

connection.start()

# Later, read latest values:
print(connection.query(obd.commands.RPM).value)

connection.stop()
```

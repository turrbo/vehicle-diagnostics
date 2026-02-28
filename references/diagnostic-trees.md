# Diagnostic Decision Trees

Structured troubleshooting flows for common vehicle symptoms. Follow each tree step-by-step, starting from the symptom.

## Table of Contents
- [Engine Won't Start](#engine-wont-start)
- [Engine Misfires / Rough Idle](#engine-misfires--rough-idle)
- [Overheating](#overheating)
- [Vibration at Speed](#vibration-at-speed)
- [Brake Issues](#brake-issues)
- [Transmission Problems](#transmission-problems)
- [Electrical / Battery Issues](#electrical--battery-issues)
- [Noise Diagnosis](#noise-diagnosis)
- [Fluid Leak Identification](#fluid-leak-identification)
- [AC Not Cooling](#ac-not-cooling)
- [Steering Problems](#steering-problems)
- [Suspension Issues](#suspension-issues)

---

## Engine Won't Start

### No Crank, No Start
1. **Check battery voltage** (should be 12.4V+ at rest, 10V+ while cranking)
   - Below 12V -> Charge/replace battery. Check alternator output (13.5-14.5V running)
   - Battery OK -> Step 2
2. **Check starter circuit**
   - Listen for click when turning key
   - No click -> Check neutral safety switch (try shifting to N), check starter relay, check fuse
   - Click but no crank -> Bad starter motor or starter solenoid. Tap starter with hammer while someone turns key (if it starts, starter is failing)
   - Multiple rapid clicks -> Weak battery or bad connection. Clean battery terminals
3. **Check key/immobilizer**
   - Security light flashing -> Immobilizer issue. Try spare key. May need dealer reset

### Cranks But Won't Start
1. **Check for spark**
   - Pull spark plug wire, ground against block, crank -> Should see spark
   - No spark -> Check coil, ignition module, crank sensor, cam sensor
   - Has spark -> Step 2
2. **Check for fuel**
   - Turn key to ON (not start), listen for fuel pump hum (2-3 seconds)
   - No hum -> Check fuel pump fuse, fuel pump relay, fuel pump (drop tank)
   - Has hum -> Check fuel pressure at rail (spec varies, typically 40-60 PSI)
   - Low/no pressure -> Clogged filter, bad pump, leaking regulator
   - Has pressure -> Step 3
3. **Check for compression**
   - Compression test: should be 125-180 PSI per cylinder, within 10% between cylinders
   - Low all cylinders -> Timing chain/belt jumped
   - Low one/two cylinders -> Head gasket, valve, or ring issue
4. **Check for air**
   - Inspect air filter (not clogged)
   - Check throttle body opens
   - Check MAF sensor connection

### Starts Then Dies
1. **IAC (Idle Air Control) valve** -> Clean or replace
2. **Vacuum leak** -> Spray carb cleaner around intake while running; RPM change = leak
3. **Fuel pressure regulator** -> Check for fuel in vacuum line (leaking diaphragm)
4. **Crank/cam sensor** -> Intermittent failure. Check for codes

---

## Engine Misfires / Rough Idle

### Single Cylinder Misfire (P030X)
1. **Identify which cylinder** from DTC code (P0301=cyl1, P0302=cyl2, etc.)
2. **Swap coil pack** with known good cylinder. Clear codes, drive
   - Misfire follows coil -> Replace coil pack
   - Misfire stays -> Step 3
3. **Swap spark plug** with known good cylinder
   - Misfire follows plug -> Replace spark plug
   - Misfire stays -> Step 4
4. **Swap fuel injector** (if accessible)
   - Misfire follows injector -> Replace/clean injector
   - Misfire stays -> Step 5
5. **Compression test** on misfiring cylinder
   - Low compression -> Valve issue, head gasket, or worn rings
   - Normal compression -> Check wiring harness to coil/injector

### Random Misfire (P0300)
1. **Check spark plugs** -> Replace if worn (gap, electrode condition)
2. **Check for vacuum leaks** -> Smoke test or carb cleaner spray test
3. **Check fuel pressure** -> Low pressure causes lean misfire on all cylinders
4. **Check MAF sensor** -> Clean with MAF cleaner
5. **Check EGR valve** -> Stuck open causes rough idle
6. **Check PCV valve** -> Stuck open causes vacuum leak

### Rough Idle Only (smooth at higher RPM)
1. **Clean throttle body** -> Carbon buildup restricts air
2. **Clean/replace IAC valve** -> Controls idle air bypass
3. **Check engine mounts** -> Worn mounts transmit normal vibration
4. **Check vacuum hoses** -> Cracked or disconnected hoses

---

## Overheating

1. **Check coolant level** (engine cold)
   - Low -> Fill and monitor. Look for leaks (Step 2)
   - Full -> Step 3
2. **Leak detection**
   - Pressure test cooling system (rent tool from auto parts store)
   - Check radiator, hoses, water pump, heater core, freeze plugs
   - Check for coolant in oil (milky dipstick = head gasket)
   - Check for white exhaust smoke (coolant burning = head gasket)
   - Block test / combustion leak test for head gasket confirmation
3. **Check thermostat**
   - Engine warm but upper radiator hose cold -> Thermostat stuck closed. Replace
   - Both hoses hot -> Step 4
4. **Check radiator fan**
   - Electric fan: should come on at ~200-210F. Check fan relay, temp sensor, fan motor
   - Clutch fan: spin when cold should have resistance. Free-spinning = bad clutch
5. **Check radiator**
   - Clogged externally -> Clean with garden hose
   - Clogged internally -> Flush. If still overheats, replace radiator
6. **Check water pump**
   - Weep hole leaking -> Replace pump
   - Impeller worn (low flow) -> Replace pump
   - Belt slipping (squealing) -> Replace/tension belt

---

## Vibration at Speed

### Vibration 40-70 MPH (improves above/below)
1. **Tire balance** -> Most common cause. Rebalance tires
2. **Bent wheel** -> Visual inspection or balance machine runout test
3. **Tire defect** -> Bulge, flat spot, separated belt. Replace tire
4. **Warped brake rotor** -> Feel pulsation in brake pedal? Measure rotor runout

### Vibration Only When Braking
1. **Warped front rotors** -> Pulsation in steering wheel. Measure runout (<0.003")
2. **Warped rear rotors/drums** -> Pulsation in brake pedal (not wheel). Measure runout
3. **Stuck caliper** -> Check for uneven brake wear, hot wheel after driving
4. **Loose lug nuts** -> Torque to spec

### Constant Vibration (increases with speed)
1. **Driveshaft balance** (RWD/AWD) -> U-joint wear, driveshaft balance weights
2. **CV joint** (FWD) -> Click when turning = outer CV. Vibration = inner CV
3. **Wheel bearing** -> Hum/growl that changes with turn direction. Jack up and check for play
4. **Tire wear pattern** -> Cupping = bad shock/strut. Feathering = alignment

### Vibration at Idle Only
1. **Engine mounts** -> Cracked/collapsed rubber. Visual inspection
2. **Transmission mount** -> Same inspection
3. **Misfire** -> See misfire section above
4. **Harmonic balancer** -> Wobble or separated rubber ring

---

## Brake Issues

### Spongy/Soft Brake Pedal
1. **Air in lines** -> Bleed brakes (start furthest from master cylinder)
2. **Low brake fluid** -> Fill and check for leaks at calipers, lines, master cylinder
3. **Bad master cylinder** -> Pedal slowly sinks to floor while holding pressure
4. **Worn brake hoses** -> Internal swelling traps pressure. Replace rubber hoses

### Brake Pedal Goes to Floor
1. **Check fluid level** -> If low, major leak. Inspect all lines and calipers
2. **Master cylinder failure** -> Internal bypass. Replace master cylinder
3. **Brake booster failure** -> Hard pedal + no assist. Check vacuum hose to booster

### Pulling to One Side
1. **Stuck caliper** -> Check for uneven pad wear. Compare rotor temps after driving
2. **Collapsed brake hose** -> Acts as one-way valve. Replace hose
3. **Contaminated pad** -> Oil/grease on pad face. Replace pads, clean rotor
4. **Uneven pad wear** -> Slide pins seized. Clean and lube caliper slides

### Grinding Noise
1. **Pads worn to metal** -> Replace pads AND rotors (rotors are likely scored)
2. **Debris between pad and rotor** -> Remove and inspect
3. **Rust ridge on rotor** -> Normal after sitting. Light braking clears it
4. **Worn brake hardware** -> Check anti-rattle clips, shims, backing plate contact

---

## Transmission Problems

### Automatic - Slipping
1. **Check fluid level and condition** (warm, engine running, in Park)
   - Low -> Top off, check for leaks at pan, cooler lines, axle seals
   - Dark/burnt smell -> Fluid degraded. Flush may help early, but may not save damaged clutches
   - Level OK, red/pink -> Step 2
2. **Check for codes** -> Solenoid codes, pressure codes, speed sensor codes
3. **Shift solenoids** -> Sticking solenoids cause specific gear slip. Often serviceable without rebuild
4. **Internal wear** -> Clutch pack, band, or torque converter failure. Rebuild or replace

### Automatic - Hard Shifting
1. **Fluid condition** -> Old fluid loses friction modifier properties. Drain and fill (NOT flush on some vehicles)
2. **Throttle position sensor** -> Erratic signal causes harsh shifts
3. **Transmission mount** -> Broken mount causes clunk during shifts
4. **Valve body** -> Sticking valves cause delayed or harsh engagement. Sometimes serviceable

### Manual - Hard to Shift
1. **Check clutch hydraulics** -> Fluid level, slave cylinder, master cylinder
2. **Clutch adjustment** -> If cable-operated, check adjustment
3. **Synchro wear** -> Grinding into specific gear = worn synchro for that gear
4. **Transmission fluid** -> Wrong type or low level. Check spec (some use ATF, some use gear oil, some use specific MTF)

### CVT Issues
1. **Fluid level and condition** -> CVT fluid is SPECIFIC. Never use regular ATF
2. **Belt/chain slip** -> Shudder under acceleration. Sometimes fluid change helps
3. **Valve body** -> Solenoid issues common on Nissan CVTs
4. **Temperature** -> CVTs overheat under heavy load. Check cooler

---

## Electrical / Battery Issues

### Battery Keeps Dying
1. **Test battery** -> Load test (most auto parts stores do free). Replace if weak
2. **Test alternator** -> 13.5-14.5V at battery with engine running
   - Below 13V -> Bad alternator or bad belt
   - Above 15V -> Overcharging, bad voltage regulator
3. **Parasitic draw test**
   - Disconnect negative cable, put multimeter in series (amp setting)
   - Normal draw: 20-50mA. Over 50mA = parasitic draw
   - Pull fuses one at a time to identify circuit
   - Common culprits: trunk/glove box light, aftermarket stereo, stuck relay, module not sleeping

### Check Engine Light On
1. **Scan for codes** -> Run DTC lookup script
2. **Pending vs confirmed** -> Pending = intermittent, confirmed = consistent failure
3. **Freeze frame data** -> Shows conditions when code set (RPM, temp, speed)
4. **Research code** -> Use forum search for make/model-specific solutions

### Electrical Gremlins (random issues)
1. **Check battery terminals** -> Clean corrosion with baking soda/water
2. **Check ground straps** -> Engine-to-chassis, battery-to-chassis, engine-to-body
3. **Check for water intrusion** -> Look at connectors, fuse boxes, under carpet
4. **CAN bus issues** -> Multiple U-codes = communication bus problem. Check wiring

---

## Noise Diagnosis

### By Location and Type

**Front end clunk over bumps**
- Sway bar end links (most common) -> Grab and shake to check play
- Ball joints -> Jack up, pry with bar to check play
- Strut mounts -> Bounce front end, listen for pop at top of strut tower
- Tie rod ends -> Grab tire at 3 and 9, shake. Check for play

**Rear clunk over bumps**
- Sway bar end links -> Same check as front
- Shock mounts -> Visual inspection for cracked rubber
- Exhaust heat shields -> Rattle = loose shield. Hose clamp fix or remove

**Squeal on startup (goes away)**
- Serpentine belt -> Glazed or worn. Replace belt and check tensioner
- Belt tensioner -> Weak spring. Replace tensioner

**Whine that increases with RPM**
- Power steering pump -> Check fluid level. Whine worst at full lock
- Alternator bearing -> Remove belt and spin by hand. Should be smooth
- Supercharger/turbo -> Normal for forced induction. Excessive = bearing wear

**Humming that changes with speed/direction**
- Wheel bearing -> Hum gets louder turning one direction (loading the bad bearing). Jack up and check for play/roughness spinning by hand

**Ticking from engine**
- Low oil -> Check level immediately
- Exhaust manifold leak -> Tick louder when cold, may quiet when warm
- Lifter/cam follower -> Tick at half engine RPM. May need adjustment or replacement
- Rod knock -> Deep knock, worse under load. Serious engine damage

---

## Fluid Leak Identification

### By Color
| Color | Fluid | Location | Urgency |
|-------|-------|----------|---------|
| Bright green | Coolant (conventional) | Radiator, hoses, water pump | Moderate |
| Orange/pink | Coolant (Dex-Cool/extended life) | Same as above | Moderate |
| Red/pink | Transmission fluid or power steering | Trans pan, cooler lines, PS pump | Moderate-High |
| Dark brown/black | Engine oil | Valve cover, oil pan, rear main seal | Low-Moderate |
| Light brown (honey) | Fresh engine oil or brake fluid | Check both sources | Brake = HIGH |
| Clear/light yellow | Brake fluid | Master cylinder, calipers, lines | HIGH - Do not drive |
| Blue | Windshield washer fluid | Reservoir, hoses | Low |
| Water (clear) | AC condensation | Under passenger side | Normal - not a leak |

### By Location
- **Front center under engine**: Oil pan, timing cover, or front main seal
- **Front at wheels**: Brake caliper, CV boot (grease), or tie rod boot
- **Center of vehicle**: Transmission pan, transfer case, or fuel line
- **Rear axle area**: Differential cover, pinion seal, or axle seals
- **Under dashboard (inside)**: Heater core (coolant with sweet smell)

---

## AC Not Cooling

1. **Check if compressor engages** -> Watch clutch when AC turned on
   - Doesn't engage -> Low refrigerant (most common), bad clutch, bad relay, bad pressure switch
   - Engages -> Step 2
2. **Check refrigerant pressure** (gauge set)
   - Low side high, high side low -> Bad compressor or expansion valve
   - Both low -> Low charge. Add refrigerant and check for leaks with UV dye
   - Both high -> Condenser blocked, fan not working, overcharge
   - Low side in vacuum -> Blockage (expansion valve or orifice tube)
3. **Check blend door** -> If air comes out but only hot, blend door actuator stuck
4. **Check cabin air filter** -> Clogged filter restricts airflow

---

## Steering Problems

### Wanders / Loose Steering
1. **Tire pressure** -> Uneven pressure causes pull. Check and equalize
2. **Alignment** -> Check for uneven tire wear patterns. Get alignment
3. **Tie rod ends** -> Grab tire at 3 and 9, shake for play
4. **Steering gear/rack** -> Center dead spot = worn gear. Fluid leak at boots = rack seals

### Hard Steering
1. **Power steering fluid** -> Low level or wrong type
2. **PS pump** -> Whining noise = pump failing
3. **PS belt** -> Slipping or broken
4. **Rack/gear** -> Internal binding. Rare but possible with age
5. **Electric PS** -> Check for codes. Motor or sensor failure

### Steering Wheel Shake
1. **At all speeds** -> Tire balance, bent wheel
2. **Only when braking** -> Warped rotor (see brake section)
3. **Only when turning** -> CV joint (FWD), U-joint (RWD)

---

## Suspension Issues

### Vehicle Leans to One Side
1. **Broken/weak spring** -> Visual comparison of ride height side-to-side
2. **Blown shock/strut** -> Bounce test (push down on corner, should rebound once)
3. **Uneven tire pressure** -> Check all four
4. **Uneven load** -> Cargo distribution

### Bouncy / Floaty Ride
1. **Worn shocks/struts** -> Bounce test. Also check for oil leaking from shock body
2. **Worn bushings** -> Control arm bushings, sway bar bushings
3. **Wrong spring rate** -> Aftermarket springs may be too soft

### Nose Dives When Braking
1. **Worn front struts** -> Lost damping ability. Replace struts
2. **Broken strut mount** -> Visual inspection at top of strut tower

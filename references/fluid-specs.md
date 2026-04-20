# Vehicle-Specific Fluid Lookup

Use this reference when the user needs an exact fluid type, viscosity, approval spec, capacity, or service-fill quantity for a specific vehicle. Do not answer from broad manufacturer habits or color-based guesses when the user is asking about a real vehicle.

## Required Inputs

Collect as many of these as possible before answering:

- Year
- Make
- Model
- Engine / displacement / engine code
- Transmission type if relevant
- Drivetrain / axle / transfer case / trim when relevant
- Which fluid is being requested

Examples:

- `2020 Honda CR-V 1.5T engine oil spec and capacity`
- `2017 Ford Escape 2.0 EcoBoost coolant type`
- `2015 Subaru Outback 2.5 CVT fluid specification`
- `2012 Silverado 1500 rear differential fluid capacity`

If the user asks "what fluid does my car take?", narrow it to the system first. Oil, ATF, CVT fluid, transfer case fluid, coolant, brake fluid, differential fluid, and power steering fluid are all separate lookups.

## Source Priority

Use sources in this order:

1. Owner’s manual, under-hood label, OEM maintenance guide, or factory service information
2. OEM parts/service portal that explicitly lists the approved spec
3. Vehicle-specific service-information publishers
4. Model-specific forum documentation only as supporting evidence, never as the only source for fluid type or capacity

For engine oil, owner’s manual and oil-cap labeling are often sufficient if they clearly match the exact engine.

## Search Patterns

Search with the exact vehicle, system, and engine/transmission when relevant. Good queries:

- `"<year> <make> <model> <engine> <fluid> capacity"`
- `"<year> <make> <model> owner's manual" "<fluid>"`
- `site:<oem-domain> "<year> <make> <model>" "<fluid specification>"`
- `"<year> <make> <model> service manual" "<fluid>"`
- `site:reddit.com/r/MechanicAdvice "<year> <make> <model>" "<fluid>"`

Tighten ambiguous queries with:

- trim
- transmission code
- axle ratio
- front / rear differential
- hybrid / diesel / turbo

## What To Return

Answer with:

1. Exact fluid specification or approval
2. Viscosity or product family if stated
3. Capacity, and whether it is total, dry fill, or service/drain-and-fill
4. Vehicle fitment used
5. Any mixing or compatibility warnings
6. Source quality statement

Template:

```text
Fluid spec: [exact spec / approval / viscosity]
Capacity: [value + units + total/service fill if known]
Applies to: [year make model engine transmission/axle/system]
Notes: [mixing warnings, OEM-only note, fill-temperature procedure, special pump/filter notes]
Source quality: [owner's manual / OEM service info / service-information source / lower-confidence supporting source]
```

## High-Risk Cases

Do not guess or generalize for:

- CVT fluid
- Dual-clutch / DSG fluid
- Transfer case fluid
- Differential fluid on limited-slip units
- European coolant approvals
- Honda/Acura power steering fluid
- OEM-specific ATF families
- Hybrid or EV thermal-management fluids

Coolant color alone is not enough. Transmission brand habits are not enough. "Most Toyotas use..." is not acceptable when the user asked about one exact vehicle.

## When Exact Spec Cannot Be Verified

Allowed fallback behavior:

- State that the exact vehicle-specific fluid spec or capacity could not be confirmed
- Say what missing detail is needed
- Recommend checking the owner’s manual, under-hood label, or factory service info

Not allowed:

- Recommending a generic equivalent as if it were confirmed
- Using color alone to identify coolant
- Assuming one transmission or axle fluid across all trims or years
- Giving a total capacity when only a drain-and-fill quantity is documented, or vice versa, without labeling it

## Sanity Checks

Before finalizing:

- Confirm the engine and transmission match the source
- Confirm whether the capacity is total, dry, refill, or drain-and-fill
- Check whether the source calls for an OEM approval standard, not just viscosity
- Check whether the system has separate front/rear diff or transfer case fluids
- Check whether the vehicle uses electric power steering and therefore no fluid

## Response Style

Give the exact spec if verified and label the confidence. If you cannot verify the fluid or capacity for the exact vehicle, say that directly rather than filling the gap with generic manufacturer guidance.

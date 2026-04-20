# Vehicle-Specific Torque Lookup

Use this reference when the user needs a torque specification for a specific vehicle and component. Do not answer from memory or from generic torque tables when a make/model/year-specific value is required.

## Required Inputs

Collect as many of these as possible before answering:

- Year
- Make
- Model
- Engine / displacement / engine code
- Drivetrain or trim when relevant
- Exact component and fastener location

Examples:

- `2018 Toyota Camry 2.5L oil drain plug torque`
- `2016 Ford F-150 3.5 EcoBoost front brake caliper bracket bolt torque`
- `2021 Honda CR-V 1.5T wheel lug nut torque`

If the user only gives a broad request such as "torque specs for my brakes", ask which fastener they need. Brake jobs often involve different specs for bracket bolts, slide pins, banjo bolts, bleeders, and wheel lugs.

## Source Priority

Use the highest-quality source available in this order:

1. OEM factory service manual, owner’s manual, or manufacturer service information
2. OEM parts or maintenance portal that explicitly states the spec
3. Service-information publishers that cite vehicle-specific data
4. Model-specific forum or enthusiast documentation only as supporting evidence, never as sole authority for a safety-critical torque value

For wheel lug torque, an owner’s manual is often acceptable if it clearly matches the exact vehicle.

## Search Patterns

Search with the exact vehicle and exact component. Good queries:

- `"<year> <make> <model> <engine> <component> torque spec"`
- `site:manualslib.com "<year> <make> <model>" "<component>" torque`
- `site:ford.com OR site:toyota.com OR site:honda.com "<year> <make> <model>" torque`
- `"<year> <make> <model> service manual" "<component>" torque`
- `site:reddit.com/r/MechanicAdvice "<year> <make> <model>" "<component>" torque`

When the first result set is ambiguous, tighten the query with one of:

- trim
- drivetrain
- engine code
- axle / front / rear
- left / right

## What To Return

Answer with:

1. Exact torque value
2. Units exactly as sourced
3. Fastener/component identity
4. Vehicle fitment used
5. Any one-time-use or torque-angle notes
6. Source quality statement

Template:

```text
Torque spec: [value + units]
Applies to: [year make model engine trim/component]
Notes: [torque-angle, replace fastener, dry/oiled threads, sequence, stage tightening]
Source quality: [OEM manual / owner's manual / service information / lower-confidence supporting source]
```

## High-Risk Cases

Do not give a guessed or generic value for these:

- Wheel lugs if exact vehicle is known but unverified
- Brake caliper bracket bolts
- Brake hose banjo bolts
- Spark plugs on aluminum heads
- Cylinder head bolts
- Connecting rod or main bearing fasteners
- Axle nuts / hub nuts
- Suspension and steering fasteners
- Drain plugs on plastic or aluminum pans
- Torque-to-yield fasteners of any kind

If you cannot verify the exact spec, say so clearly and stop short of inventing one.

## When Exact Spec Cannot Be Verified

Allowed fallback behavior:

- State that the exact vehicle-specific torque spec could not be confirmed
- Explain what additional detail is missing
- Recommend obtaining the factory service info or owner’s manual

Not allowed:

- Giving a generic range as if it were correct for that vehicle
- Mixing values from different engines, trims, or generations without saying so
- Treating forum memory as authoritative for safety-critical fasteners

## Sanity Checks

Before finalizing:

- Confirm the vehicle generation matches the source year range
- Confirm the component location matches front vs rear, left vs right, upper vs lower
- Check whether the spec is in `ft-lb`, `in-lb`, or `N·m`
- Check for a torque-plus-angle step
- Check whether the source assumes new bolts, dry threads, or lubricant/threadlocker

## Response Style

Keep it direct. If the source is strong, provide the number and the notes. If the source is weak or incomplete, say that the value is not verified for the exact vehicle and say what detail or document is needed to finish the lookup.

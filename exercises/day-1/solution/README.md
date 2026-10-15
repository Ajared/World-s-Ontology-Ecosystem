# Day 1 Solution: Patrol Boat

`patrol-boat-solution.ttl` is the starter ontology with Parts 2–6 of the exercise completed. Open it in Protégé from this folder. `catalog-v001.xml` resolves the BFO import to `../starter/imports/bfo-core.ttl`.

## What was added

| Part | Axioms |
|---|---|
| 2. Class hierarchy | `PatrolBoat ⊑ material entity`, `ActOfMotion ⊑ process`, `MeasurementDatum ⊑ generically dependent continuant`, `SpeedMeasurementDatum ⊑ MeasurementDatum`, `DurationMeasurementDatum ⊑ MeasurementDatum`, `MeasurementUnit ⊑ generically dependent continuant` |
| 3. Individuals | `patrol_boat_01`, `motion_01`, `speed_measurement_01`, `duration_measurement_01`, `knot`, `hour`, each with exactly one asserted type |
| 4. Object properties | `patrol_boat_01 participates in motion_01`; both measurements `is about motion_01`; units `knot` and `hour` |
| 5. Data properties | speed `has decimal value 12.0`, duration `has decimal value 1.0` (both `xsd:decimal`) |
| 6. Definition | `MovingPatrolBoat ≡ PatrolBoat and 'participates in' some ActOfMotion` |

## Reasoner results (HermiT)

| Check | Result |
|---|---|
| Completed ontology | Consistent, no unsatisfiable classes. `patrol_boat_01` is inferred to be a `MovingPatrolBoat`. |
| Dependency test (remove `patrol_boat_01 participates in motion_01`) | Consistent. The inferred `MovingPatrolBoat` type disappears. |
| Category error (add `motion_01 Type SpeedMeasurementDatum`) | Inconsistent: `motion_01` would be both a process (occurrent) and a generically dependent continuant, and BFO declares continuant and occurrent disjoint. |
| Repair (remove only that type assertion) | Consistent again, and the `MovingPatrolBoat` inference returns. |

The submitted file is the repaired version.

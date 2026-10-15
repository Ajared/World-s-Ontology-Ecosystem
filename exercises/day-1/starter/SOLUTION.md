# Day 1 worked solution

Open `patrol-boat-solution.ttl` from this directory. The adjacent catalog maps
the BFO import to the bundled `imports/bfo-core.ttl` file.

The ontology places boats under BFO material entity, motion under process, and
measurement data and units under generically dependent continuant. A boat
participates in a motion process; speed and duration data are about that
process. The decimal values and units belong to the data, not to the process.

`MovingPatrolBoat` is defined equivalently as a patrol boat that participates
in some act of motion. Thus, after classifying with an OWL reasoner,
`patrol_boat_01` is inferred to be a moving patrol boat without that type being
asserted directly.

To reproduce the category error from the exercise, temporarily add
`SpeedMeasurementDatum` as a type of `motion_01`. The ontology becomes
inconsistent because the motion is an occurrent while the measurement datum is
a continuant, and BFO makes those categories disjoint. Remove only that added
type assertion to restore consistency. The supplied solution file represents
the repaired, consistent state.

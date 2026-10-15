# Day 5 Capstone

## Participants

Individual submission.

## Model

- OWL: [`capstone-model.owl`](capstone-model.owl) (Turtle syntax). It imports BFO; `catalog-v001.xml` resolves the import to `../../day-1/starter/imports/bfo-core.ttl`.
- Diagram: [`capstone-pattern.svg`](capstone-pattern.svg)
- Operational view query: [`operational-view.rq`](operational-view.rq)

**Size:** 11 local classes (10 primitive plus the defined `pump inspection`), 6 local object properties (`is about`, `prescribes`, `has specified output` and its inverse, `recommends`, `requests`), BFO `has participant`, `realizes`, `bearer of` and `has continuant part`, 3 data properties, and 10 named individuals.

| Scenario element | Representation | Kind |
|---|---|---|
| Maintenance procedure ("every 30 days") | `pump_inspection_procedure` : *inspection procedure* ⊑ GDC, `has interval in days 30` | information (prescription) + literal |
| Technician Alex | `alex` : *person*, `bearer of alex_technician_role` : *technician role* | object + role |
| Inspection 17 | `inspection_17` : *inspection* ⊑ process. It has participants Alex and P-17 and realizes Alex's technician role. | process |
| Pump P-17 | `pump_p17` : *pump* ⊑ object, `bearer of vibration_p17` : *vibration* ⊑ quality | object + quality |
| Report R-17 | `report_r17` : *inspection report* ⊑ GDC; specified output of Inspection 17; `is about` P-17 | information artifact |
| 4.2 mm/s | `vibration_measurement_r17` : *vibration measurement datum*, part of R-17, `is about vibration_p17`, `has decimal value 4.2`, `has unit label "mm/s"` | measurement datum + literals |
| "requires bearing replacement" | R-17 `recommends replace_bearing_p17` : *maintenance action specification* | prescription (not a fact) |
| Work Order W-22 | `work_order_w22` : *work order* ⊑ GDC, `requests replace_bearing_p17`, `is about` P-17 | information artifact |

The bearing replacement has **not happened**, so it is not a process individual. Both the report and the work order point to a *specification* of the action, which is information. When the replacement is carried out, a process individual can be added and linked to the specification with `prescribes`.

**Competency questions:**

1. Inspection procedure: `pump_inspection_procedure prescribes inspection_17`.
2. Performed by: `inspection_17 has participant alex`, realizing `alex_technician_role`.
3. Inspected: `inspection_17 has participant pump_p17`; inferred to be a *pump inspection*.
4. Resulting information: `inspection_17 has specified output report_r17`.
5. Vibration value: `report_r17 has continuant part vibration_measurement_r17` → `4.2` / `"mm/s"`.
6. Requested action: `work_order_w22 requests replace_bearing_p17` ("Replace bearing").
7. Which work order: `work_order_w22`.

## Three Definitions

1. **inspection** (class): *A process in which a participant examines a material entity in order to produce information about the condition of that entity.*
   Genus: process. Differentia: examining a material entity in order to produce condition information. This agrees with the axioms: `inspection ⊑ process`, and its output is an information entity.
2. **work order** (class): *A generically dependent continuant that requests that the maintenance action specified by some maintenance action specification be carried out.*
   Genus: generically dependent continuant. Differentia: it *requests* a specified action. This keeps the work order (information) apart from the repair (a future process), and it agrees with `work order ⊑ requests some maintenance action specification`.
3. **prescribes** (relation): *A relation that holds between a directive information entity and a process when the process is carried out in accordance with what the information entity directs.*
   It states when the relation holds rather than restating its domain and range, and it is used only for a process that actually occurred (Inspection 17). That is why the requested replacement is linked to a specification and not to a process.

## AI Comparison

The AI proposal was produced by Claude Opus 5.5 from the simple prompt in the exercise, with the scenario pasted in. Summary of its proposal:

> **Classes:** Pump, Bearing, Person, Technician (⊑ Person), MaintenanceProcedure, Inspection, InspectionReport, VibrationMeasurement, MaintenanceAction, BearingReplacement (⊑ MaintenanceAction), WorkOrder.
> **Individuals:** Alex (Technician), P-17 (Pump), Inspection17, R-17, VibrationMeasurement17, BearingReplacement17 (BearingReplacement), W-22.
> **Relations:** performedBy, inspects, followsProcedure, produces, recordsMeasurement, recommends, requests, hasPart (Pump → Bearing).
> **Data properties:** hasValue (4.2), hasUnit ("mm/s"), hasInterval ("30 days"), and `P-17 hasVibrationLevel 4.2` "for quick lookup".
> **Key decision:** "W-22 requests BearingReplacement17, the maintenance action to be performed on P-17."

### Difference 1

**AI suggestion:** `Technician` is a subclass of `Person`, and Alex is typed directly as a Technician.
**Decision:** MODIFY
**Reason:** Being a technician is a role that a person bears, not a kind of person. Alex keeps being a person when off duty, and the same person can bear several job roles. I kept *person* for Alex and added a *technician role* that Alex bears and Inspection 17 realizes.

### Difference 2

**AI suggestion:** `BearingReplacement17` is created as an individual of `MaintenanceAction` (a process), and W-22 `requests` it.
**Decision:** REJECT
**Reason:** No replacement has happened. Creating a process individual asserts that one exists, which turns a prescription into an apparent observed fact. W-22 and R-17 instead point to a *maintenance action specification*, which is information. A replacement process can be added once it occurs, linked by `prescribes`.

### Difference 3

**AI suggestion:** In addition to the measurement, the pump gets a shortcut data property `P-17 hasVibrationLevel 4.2`.
**Decision:** REJECT
**Reason:** It confuses the pump's vibration (a quality, which changes over time) with one measured value of it, and it drops the provenance: which inspection, which report, and which unit. The value stays on the measurement datum, which is about the pump's vibration quality. A quick-lookup field belongs in the operational view (Part 5), derived by query, not asserted in the authoritative model.

*Also noted:* the AI's `Bearing` (part of the pump) is a reasonable refinement, because the replacement is strictly about the bearing. It was left out to keep the pattern minimal, and the action specification is about the pump.

## Reasoner Results

HermiT, with BFO imported:

- **Consistent:** Yes.
- **Unsatisfiable classes:** None.
- **Expected inferences:** `Inspection 17` is inferred to be a *pump inspection* (defined as an inspection with a pump participant).
- **Unexpected inferences:** None. As a test, typing `inspection_17` as a *work order* made the ontology inconsistent (process vs. generically dependent continuant), so the category boundaries are enforced.

Consistency only shows that the axioms do not contradict each other. Creating a `BearingReplacement17` process individual (Difference 2) would have stayed consistent and still been wrong.

## Operational View

| Application field | Ontology source |
|---|---|
| Pump | `rdfs:label` of the `Pump` that participates in the inspection: `pump_p17` → "Pump P-17" |
| Last inspection | `rdfs:label` of the `Inspection` with that pump as participant: `inspection_17` → "Inspection 17" |
| Measured vibration | `has decimal value` + `has unit label` of the `VibrationMeasurementDatum` that is a continuant part of the inspection's specified output: `vibration_measurement_r17` → "4.2 mm/s" |
| Maintenance action | `rdfs:label` of the `MaintenanceActionSpecification` requested by the work order: `replace_bearing_p17` → "Replace bearing" |
| Work order | `rdfs:label` of the `WorkOrder` that is about the pump and requests that action: `work_order_w22` → "Work Order W-22" |

`operational-view.rq` derives exactly this row from the model. Running it returns `Pump P-17 | Inspection 17 | 4.2 mm/s | Replace bearing | Work Order W-22`.

### What information was omitted?

- Who performed the inspection (Alex) and the technician role it realized.
- The procedure that prescribed the inspection and its 30-day interval.
- Report R-17 as an artifact, and the fact that the measurement is part of it.
- The vibration as a quality of the pump, as distinct from the measured value.
- The difference between the report *recommending* the replacement and the work order *requesting* it, and the fact that the replacement has not yet happened.
- Provenance: which process produced which information.

### Is the operational view lossy?

**YES.** Each field flattens a path in the ontology into a string. The view cannot answer competency questions 1 and 2, and it cannot be turned back into the model: from "4.2 mm/s" alone you cannot tell which report it came from or what it was about.

### Is the operational view divergent?

**NO**, with two conditions. Every field value is the same as a value in the ontology, so it does not change the meaning, provided that:
1. "Maintenance action: Replace bearing" is read as the *requested* action. If the application showed it as performed, it would diverge.
2. "Last" in "Last inspection" adds a claim of recency that the model does not contain, since there are no inspection dates. It is only correct here because there is a single inspection. A real system would need inspection dates in the model to derive it.

**Explanation:** A simplified view may drop detail but must not add or change claims. This view drops a lot, but it changes nothing, as long as the two labels above are read correctly.

## Most Important Lesson from the Week

A reasoner can only enforce distinctions that someone has already decided to encode. In this scenario, the AI proposal, the operational view, and a consistent ontology could each have quietly turned the recommended bearing replacement into a repair that never happened. The modeling judgment (process vs. information, role vs. bearer, prescription vs. fact) comes first, and the logic only keeps those decisions from being lost later.

# Day 2 Solution: Cases 2 and 3

| Case | Pattern | OWL |
|---|---|---|
| 2: Airbus A321-111, designed vs. measured maximum approach speed | [`case-2-pattern.svg`](case-2-pattern.svg) | [`case-2.owl`](case-2.owl) |
| 3: SOC entries that mention "Aerospace Engineer" | [`case-3-pattern.svg`](case-3-pattern.svg) | [`case-3.owl`](case-3.owl) |

The OWL files use Turtle syntax, which Protégé detects automatically. Both import BFO. `catalog-v001.xml` resolves that import to `../bfo-core+.ttl`, which also provides `is about`. Every local class, property, and named individual has an `skos:definition`. For individuals, the definition serves as the identifying description and names the source row.

## Case 2

Source: `aircraft_data.xlsx`, row 13 (`Model_BADA` = Airbus A321-111, `Approach_Speed_maximum_knot` = 142), plus the case statement: five approaches with an average maximum approach speed of 139 kt.

Modeling decisions:

- **What was designed is kept apart from what was measured.** The 142 kt value belongs to a *maximum approach speed specification*, a directive information entity that is part of the *aircraft design specification*. It is not a property of the airframe. The 139 kt value belongs to an *average approach speed datum*, which is about the *approach test process*.
- **The test is a process with five approaches as occurrent parts.** The aircraft participates in the test and in each approach.
- **The five per-approach measurements exist, but their values are not in the source, so they are not asserted.** The average is linked to them with `is derived from`. Calculating the average belongs in a query (e.g. SPARQL `AVG`), not in OWL.
- **Conformance is something the reasoner can derive.** `within-design-limit average approach speed datum` is defined as an average approach speed datum with `has decimal value some xsd:decimal[<= 142]`.

Reasoner (HermiT): consistent, with no unsatisfiable classes. `average approach speed 1` (139 kt) is inferred to be a *within-design-limit average approach speed datum*. When the value is changed to 150 as a test, the inference no longer appears.

## Case 3

Source: `soc_structure_definitions.xlsx`, sheet *SOC Definitions*, rows 188 (17-2010), 189 (17-2011) and 229 (17-3021).

Modeling decisions:

- **A SOC entry is an information entity.** Its code, title, level, and definition text are literals. The occupation itself is represented by the job role that the entry is about: `is about only (bearer of some <role>)`, following the Day 2 solution pattern.
- **17-2010 and 17-2011 are separate entries with the same title.** The broad group 17-2010 contains exactly one detailed occupation, 17-2011, which is modeled as `continuant part of` 17-2010. Both entries are about the same role, *aerospace engineer role*. Only the detailed entry has a definition.
- **The "Aerospace Engineer" string match in 17-3021 is misleading.** Its definition describes operating, installing, adjusting, and maintaining test and launch equipment, which is technician work. It is therefore about an *aerospace engineering technician role*, which falls under *technician role*, and *technician role* is declared disjoint from *engineer role*.
- **The SOC definitions' "May …" clauses are optional duties, so they are not encoded as necessary conditions.** Each role is restricted to `has realization only` the process type named by the definition's required duties.
- **Broad and detailed are defined classes.** They are defined by the `has SOC level` value, so the reasoner classifies each entry.

Reasoner (HermiT): consistent, with no unsatisfiable classes. 17-2010 is inferred to be a *broad occupation entry*, and 17-2011 and 17-3021 are inferred to be *detailed occupation entries*. As a test, a role asserted to be both an aerospace engineer role and an aerospace engineering technician role makes the ontology inconsistent, as intended.

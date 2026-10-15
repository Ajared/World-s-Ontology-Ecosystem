# Day 3 Evaluation: Clinic Appointment Ontology

Files: [`prompt.md`](prompt.md), [`generated-ontology.owl`](generated-ontology.owl) (original output, unchanged), and [`revised-ontology.owl`](revised-ontology.owl). Both OWL files are written in Turtle syntax. The revised file imports BFO, and `catalog-v001.xml` resolves that import to `../../day-1/starter/imports/bfo-core.ttl`.

## Step 2: Intended model (recorded before inspection)

- **Represents:** outpatient appointments at one clinic, keeping what was *booked* (scheduling data) apart from what *happened* (the visit).
- **Questions:** the five competency questions in `prompt.md`. They cover booked patient, clinician, and time; whether a booking was kept, cancelled, or missed; who took part and in what capacity; the recorded reason and which record states it; and which room the visit used.
- **Central terms:** patient, clinician, appointment/booking, visit, cancellation, no-show, examination room, reason for visit, visit record.
- **Assumptions given to the model:** BFO alignment; definitions for everything; illustrative individuals; domain and range axioms where appropriate.
- **Guidance the prompt omits:** It does not say to *import* BFO (it allowed declaring BFO classes instead). It does not mention roles vs. bearers, does not ask for the booking/visit distinction to be expressed logically, and does not warn against status strings.

## Step 4: Reasoner before revision (HermiT)

| Check | Result |
|---|---|
| Consistent | Yes |
| Unsatisfiable classes | None |
| Unexpected equivalences | `Appointment ≡ Visit`, as asserted. As a result, every cancelled appointment is entailed to be a visit. |
| Expected classifications | None are possible: there are no defined classes, so the reasoner cannot classify anything. |
| What it fails to detect | Everything in the issue list below. As a test, `Appointment_001` was also typed as a `ReasonForVisit` (a process that is also information), and the ontology **stayed consistent**. With BFO imported, the same assertion is inconsistent. |

## Step 5–6: Five substantive problems

### 1. Category error: booking conflated with visit, and an unjustified equivalence (ontological + logical)

`Appointment ⊑ process`, and `Visit ≡ Appointment`. An appointment as *booked* is a plan, which is information that exists before the visit and continues to exist if the visit never happens. A visit is the process. Because of the equivalence, `CancelledAppointment ⊑ Visit ⊑ process`, so `Appointment_002` is entailed to be a visit that took place, which is the opposite of what the data says. It is also asserted to `occursIn Room3`.

**Fix:** `AppointmentBooking ⊑ generically dependent continuant` and `ClinicVisit ⊑ process`, linked by `prescribes`. The equivalence is removed. A cancelled booking prescribes no visit, so no process individual exists for it.

### 2. Role confused with its bearer (ontological)

`Patient ⊑ Person` and `Clinician ⊑ Person`. Being a patient is not a kind of human being. The same person can be a patient on Monday and a clinician on Tuesday. `PatientRole` is declared but never used, so it duplicates `Patient`.

**Fix:** `PatientRole` and `ClinicianRole` are subclasses of BFO `role` and are disjoint. Persons are *bearers of* them, and a clinic visit *realizes* them.

### 3. Definitions that are circular, vague, or define the word (definitions)

- *Appointment*: "An appointment is a scheduled meeting …" defines the word, and its genus (meeting, a process) contradicts the intended meaning (a booking).
- *Visit*: "A visit by a patient to the clinic" is circular.
- *Visit Record*: "A record of a visit" is circular.
- *Reason For Visit*: "Information **related to** why the patient is visiting, **usually** a symptom or complaint" is vague and hedged.
- *Patient Role*: "The role of being a patient" is circular.

**Replacement example:** *visit record*: "A generically dependent continuant that documents what took place during a particular clinic visit." It names the closest genus, states the differentia (what it documents), avoids the defined term, and agrees with the axiom `VisitRecord ⊑ is about some ClinicVisit`.

### 4. Relations: a vague catch-all relation and domains that exclude the right things (relations)

- `relatedTo` (symmetric, no definition beyond "a general relation") is the only link from `Record_001` to its appointment, and it carries no meaning. Because it is symmetric, it also makes the appointment "related to" the record.
- `hasPatient`, `hasClinician`, and `occursIn` all have domain `Appointment`. Asserting a room or a patient on a *cancelled* appointment therefore makes claims about a visit that never occurred.
- `hasReason` relates a process directly to an information entity, which hides who stated the reason and in which record.

**Fix:** `relatedTo` is replaced by `is about` (record → visit). The booking relations (`books patient/clinician/room`) are sub-properties of `is about` with domain `AppointmentBooking`, and participation in the visit uses BFO `has participant`, `realizes`, and `occurs in`. The reason is a `ReasonForVisitStatement` that the booking and the record `state`.

### 5. Individuals and literals: status strings duplicate classes, and a label is turned into an individual (individuals/values)

`hasStatus "completed"/"cancelled"` duplicates the `CancelledAppointment` class with nothing keeping them consistent. Nothing stops an instance of `CancelledAppointment` from having status `"completed"`. The individual `:Completed` has no type and stands for nothing but a status label.

**Fix:** `:Completed` is removed. Status is kept as source data (`has booking status`, functional), and `CancelledAppointmentBooking`, `MissedAppointmentBooking`, and `FulfilledAppointmentBooking` are *defined* classes, so the reasoner derives them from the data instead of asserting them alongside it.

### 6. (Logical, additional) BFO is declared but not imported

The generated file copies five BFO class IRIs with no axioms, so BFO's disjointness (continuant vs. occurrent, etc.) does not apply. That is why the reasoner could not detect issue 1 or the test assertion above. The revision imports BFO.

## Step 7: Reasoner after revision (HermiT)

| Check | Result |
|---|---|
| Consistent | Yes |
| Unsatisfiable classes | None |
| Expected classifications | `Booking_001` is inferred to be a **fulfilled** booking because it prescribes `Visit_001`. `Booking_002` is inferred to be a **cancelled** booking from its status. |
| Unexpected consequences | When testing the first revision, `Booking_002` could also prescribe a visit, and the reasoner then classified it as both cancelled **and** fulfilled without complaint. A disjointness axiom was added for fulfilled, cancelled, and missed bookings, and that test now makes the ontology inconsistent. No other unexpected inferences appeared. |
| Category test | Typing a booking as a process is now inconsistent, because BFO's continuant/occurrent disjointness applies. |

## What the reasoner could and could not do

The reasoner found none of the five problems in the generated ontology. Every one of them needed ontological or domain judgment: knowing that a booking is not a visit, that a patient is a role, and that a definition is circular. Once those distinctions were written as axioms (imported BFO, disjointness, defined classes), the reasoner could enforce them and catch the remaining gap in the revision.

Of the five problems, the prompt caused issues 2 and 6: it never mentioned roles and explicitly allowed declaring BFO instead of importing it. The generated model caused issues 1, 3, 4, and 5, despite the prompt stating the booked-vs.-happened purpose plainly.

# Prompt

## Model

Claude Opus 5.5 (`claude-opus-5-5`), run in the same session that later evaluated the output. The generation step used only the prompt below; nothing from the evaluation was available to it at that point. The output was saved unchanged as `generated-ontology.owl`.

Caveat: the same model family both generated and evaluated the ontology. A stricter run would use a different model or a fresh session for generation.

## Prompt text

```text
Create an OWL ontology for outpatient medical appointments at a single clinic.

Purpose: the clinic wants to integrate its scheduling system with its visit
records, so the ontology must keep apart what was booked from what actually
happened.

The ontology should support questions such as:
1. Which patient is booked with which clinician, and for what time?
2. Did a booked appointment actually take place, or was it cancelled or missed?
3. Who took part in a visit, and in what capacity (patient, clinician)?
4. What reason for the visit was recorded, and which record states it?
5. Which visits happened in which examination room?

Requirements:
- Serialize the ontology in Turtle so that it opens in Protégé.
- Align the top-level classes with Basic Formal Ontology (BFO 2020); you may
  declare the BFO classes you use with their OBO IRIs instead of importing BFO.
- Include an rdfs:label and a textual definition (skos:definition) for every
  class and property you create.
- Include a few named individuals that illustrate one booked appointment that
  took place and one that was cancelled.
- Use domain and range axioms where appropriate.
```

## Follow-up prompts

None. The output parsed on the first attempt, so no syntax-repair prompt was needed.

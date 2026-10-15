# Day 4 Exercise: Ground, Critique, Validate

Use this guide with the [Day 4 overview](README.md). The exercise compares
abductive hypotheses from AI agents with constraint validation and a separate
OWL entailment check. The ontology stages and experiment settings are already
provided; you do not need to rebuild the Zebra Puzzle ontology.

## 1. Inspect the experiment

Read the experiment table and workflow overview in `README.md`, then inspect
`exercise.json`. Find the four experiment definitions and note which stages,
ontology grounding, Critic, and SHACL validation each one uses. Read the
hypothesis and Critic prompts, paying particular attention to the difference
between a plausible preference, a possible arrangement, and an entailed fact.

## 2. Prepare and run

Install [UV](https://docs.astral.sh/uv/) if it is not already available. From
this directory, prepare and verify the offline setup:

```bash
make install verify-setup test
```

Then configure the model provider and credentials as described in `README.md`
and `config.yaml`, and run:

```bash
make
```

Keep credentials in the local `.env` file; do not add them to a commit. Each
run creates a timestamped directory under `runs/` containing a consolidated
CSV and detailed records for each experiment and ontology stage.

## 3. Compare the four experiments

Use `agent-run-log.csv` and the experiment-specific artifacts to compare:

1. **LLM only:** What does the model claim without ontology evidence?
2. **Ontology-grounded:** Which claims now cite axioms, and do those citations
   support the reasoning steps?
3. **Critic added:** What errors does the Critic identify? Does the revision
   address the named evidence or reasoning problem?
4. **SHACL feedback loop:** Which concrete arrangement violations are
   reported, and how does the proposal change over the cumulative stages?

For each claim, distinguish supporting evidence from assumptions and
unresolved ties. A SHACL-conforming arrangement establishes that one candidate
is possible for that arrangement; it does not establish uniqueness or logical
entailment. An LLM Critic is also not a formal validator.

## 4. Run the separate deductive check

Open `ontology/zebra-round-4.owl` in Protégé, start an OWL 2 DL reasoner, and
query:

```text
Resident and livesIn some (hasPet value Zebra)
```

Compare the result with the final abductive hypothesis and SHACL evidence.
State whether the answer is merely plausible, supported as possible by a
conforming arrangement, or entailed by the ontology. Explain what evidence
supports that status.

## 5. Reflect

In your notes, answer:

- What did ontology grounding add to the LLM-only response?
- What did the Critic catch that the workflow could verify, and what remained
  outside its reach?
- How did SHACL feedback change the proposed arrangement?
- Did the final OWL query entail a unique owner? What axioms support your
  answer?
- Where did the abductive and deductive results agree or differ?

# AI Prompt-and-Response Log

**Model:** Claude Opus 5.5 (`claude-opus-5-5`).

**Contamination note:** The model recognizes the Zebra Puzzle and knows its published solution. Every prompt included the required instruction not to use that knowledge, and the responses below reason only from the supplied clues. That cannot be verified from outside, though. The masked identifiers in `../ontology/` exist to prevent exactly this, so a cleaner run would use them with a different model.

Each run received the OWL file for that stage (`zebra-stage-N.owl`) together with the prompt.

Common preamble used in every run:

```text
Do not search the web, retrieve a memorized solution, or rely on prior knowledge
of the Zebra Puzzle. Reason only from the clues supplied in this prompt.
```

---

## Run 1: Stage 1 (clues 1–5)

**Prompt**

```text
[preamble]
[contents of zebra-stage-1.owl]

Who owns the zebra? Make the best abductive guess you can from only these clues.
Explain your reasoning, identify any assumptions you make, and state how confident
you are.
```

**Response**

> None of the clues mention the zebra. What they do establish:
>
> - Each house has exactly one pet and each pet is in exactly one house (the cardinality axioms).
> - The Spaniard lives in the house with the dog (clue 3), so the Spaniard cannot own the zebra.
>
> That leaves the Englishman, the Ukrainian, the Norwegian, and the Japanese. The clues about the Englishman (red house) and the Ukrainian (tea) do not interact with pets at all, and the Norwegian and Japanese are unconstrained. Nothing favours any of the four.
>
> **Best guess:** if I have to name one, the Norwegian. This is an arbitrary tie-break, not an inference.
> **Assumptions:** the one-pet-per-house constraint, which the ontology states explicitly.
> **Confidence:** about 25%, the same as a uniform guess over the four remaining candidates.

## Run 2: Stage 2 (clues 1–8)

**Prompt**

```text
[preamble]
[contents of zebra-stage-2.owl]

Who owns the zebra? Make the best abductive guess you can from only these clues.
Explain your reasoning, identify any assumptions you make, and state how confident
you are. Do not preserve your earlier answer merely for consistency.
```

**Response**

> The new clues are: green is immediately right of ivory (6), the Old Gold smoker keeps snails (7), and Kools are smoked in the yellow house (8).
>
> Clue 7 only says that whoever smokes Old Gold does not own the zebra, but no clue yet ties Old Gold to a nationality, so it removes no candidate. Clues 6 and 8 constrain colours and smokes but never touch pets or the four remaining nationalities in a way that separates them.
>
> **Best guess:** the four candidates (Englishman, Ukrainian, Norwegian, Japanese) are still effectively tied. I have no evidence-based reason to change my nominal pick. I am keeping the Norwegian because nothing new distinguishes the candidates, not to stay consistent with my earlier answer.
> **Assumptions:** "immediately to the right" is read as one position further from House 1.
> **Confidence:** about 25%.

## Run 3: Stage 3 (clues 1–11)

**Prompt**

```text
[preamble]
[contents of zebra-stage-3.owl]

Who owns the zebra? Make the best abductive guess you can from only these clues.
Explain your reasoning, identify any assumptions you make, and state how confident
you are. Do not preserve your earlier answer merely for consistency.
```

**Response**

> New facts: milk is drunk in House 3 (9), the Norwegian lives in House 1 (10), and the Chesterfields smoker lives next to the fox owner (11).
>
> What follows:
>
> - Coffee is drunk in the green house and milk in House 3, so green is not House 3. With green immediately right of ivory, (ivory, green) is (1, 2), (3, 4) or (4, 5).
> - The Englishman lives in the red house, and the Norwegian is in House 1, so House 1 is not red.
> - The Ukrainian drinks tea, so the Ukrainian is not in House 3.
>
> None of this places the zebra. The fox is now tied to the Chesterfields smoker's neighbour, so whoever smokes Chesterfields does not own the fox, but that removes no zebra candidate.
>
> **Best guess:** revising freely, I could argue the Norwegian is *less* likely now. Being at the end of the row, House 1 has only one neighbour, which slightly limits where the fox can be relative to Chesterfields. That effect is tiny, though, and the evidence is still nearly uniform. Nominal pick: the Japanese, the candidate with the fewest constraints, so the most possible arrangements.
> **Assumptions:** the houses form a single row, with House 1 at one end.
> **Confidence:** about 25–30%. This is an abductive preference, not a derivation.

## Run 4: Stage 4 (clues 1–15)

**Prompt**

```text
[preamble]
[contents of zebra-stage-4.owl]

Who owns the zebra? Make the best abductive guess you can from only these clues.
Explain your reasoning, identify any assumptions you make, and state how confident
you are. Do not preserve your earlier answer merely for consistency.
```

**Response**

> The clues are now enough to derive the answer rather than guess it.
>
> 1. Norwegian in House 1 (10). The Norwegian lives next to the blue house (15), so House 2 is blue.
> 2. Green is right of ivory (6), green is not House 3 (milk, 9), and House 2 is blue, so (ivory, green) is (3, 4) or (4, 5).
> 3. House 1 is not red (Englishman), blue, ivory, or green, so it is yellow. Kools are smoked in House 1 (8), and the horse is in House 2 (12).
> 4. House 1's drink is not tea (Ukrainian), coffee (green), or milk. If it were orange juice, Lucky Strike would be smoked there (13), but House 1 smokes Kools. So House 1 drinks water.
> 5. **Case ivory 3 / green 4 / red 5:** the Englishman is in 5. House 5 cannot drink tea (not the Ukrainian), so it drinks orange juice and smokes Lucky Strike. House 2 drinks tea, so the Ukrainian is in 2. House 2 keeps the horse, so it is not Old Gold (snails), and the Ukrainian is not the Japanese, so it is not Parliaments; House 2 therefore smokes Chesterfields. Houses 3 and 4 then hold Old Gold and Parliaments, and the Spaniard and the Japanese. The Japanese smokes Parliaments, so the Spaniard smokes Old Gold and keeps snails. This contradicts clue 3 (dog). Rejected.
> 6. **Case ivory 4 / green 5 / red 3:** the Englishman is in 3, and coffee is in 5. Houses 2 and 4 drink tea and orange juice.
>    - If House 2 drinks orange juice, it smokes Lucky Strike and the Ukrainian is in 4. The Japanese cannot be in 2 (Parliaments ≠ Lucky Strike), so the Japanese is in 5 and the Spaniard in 2. The Spaniard's dog would then be in the horse's house. Rejected.
>    - So House 2 drinks tea (Ukrainian), and House 4 drinks orange juice (Lucky Strike). House 2 smokes Chesterfields (not Old Gold because of the horse, not Parliaments because the Ukrainian is not the Japanese). Houses 3 and 5 hold Old Gold and Parliaments. The Englishman is in 3, so House 3 smokes Old Gold and keeps snails, and the Japanese is in 5 with Parliaments. The Spaniard is in 4 with the dog. Chesterfields (2) is next to the fox, and House 3 has snails, so the fox is in House 1.
> 7. The only pet left for House 5 is the zebra.
>
> **Answer:** the **Japanese** owns the zebra (House 5, green, coffee, Parliaments). The Norwegian drinks water.
> **Assumptions:** the one-to-one constraints and the row order encoded in the ontology. Nothing beyond the clues was used.
> **Confidence:** very high. Every alternative branch leads to a contradiction, so this is a deduction, not a guess.

---

## Comparison with HermiT and with the space of possible solutions

To see what an abductive guess *could* justify at each stage, all arrangements consistent with each stage's clues were enumerated by brute force (outside OWL):

| Stage | Clues | Consistent arrangements | Share where each candidate owns the zebra (Eng / Spa / Ukr / Nor / Jap) | AI pick | HermiT: `Person and livesIn some (hasPet value Zebra)` |
|---|---|---:|---|---|---|
| 1 | 1–5 | 37,324,800 | 0.25 / 0 / 0.25 / 0.25 / 0.25 | Norwegian (~25%) | no instances |
| 2 | 1–8 | 300,672 | 0.23 / 0 / 0.26 / 0.25 / 0.25 | Norwegian (~25%) | no instances |
| 3 | 1–11 | 2,400 | 0.25 / 0 / 0.26 / 0.27 / 0.23 | Japanese (~25–30%) | no instances |
| 4 | 1–15 | 1 | 0 / 0 / 0 / 0 / 1 | Japanese (deduced) | **Japanese** |

Observations:

- For stages 1–3 the model's stated confidence (~25%) matched the actual spread of possibilities. Its stage 3 reasoning ("the Japanese has the fewest constraints") sounded plausible but was not supported: by count, the Japanese was the *least* likely candidate at that stage (23%). This is a clear case of a plausible-sounding abductive rationale that the evidence does not back.
- HermiT never guessed. It returned no answer until the axioms entailed one, and at stage 4 it entailed exactly the arrangement the model derived.
- The model and the reasoner agree only once the problem is fully determined. Before that, the model gives an answer and the reasoner gives none, and a confident-sounding answer from the model would be easy to mistake for an entailment.

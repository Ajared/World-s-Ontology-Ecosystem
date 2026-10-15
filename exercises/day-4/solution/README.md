# Day 4 Solution: Zebra Puzzle (manual workflow)

This follows `../exercise-instructions.md`: build the puzzle in OWL in four clue groups, run HermiT after each group, and compare the results with an AI model's abductive guesses.

| File | Contents |
|---|---|
| `zebra-stage-1.owl` | Part 1: clues 1–5 |
| `zebra-stage-2.owl` | Part 3: clues 1–8 |
| `zebra-stage-3.owl` | Part 4: clues 1–11 |
| `zebra-stage-4.owl` | Part 5: all 15 clues (the completed ontology) |
| `ai-log.md` | The four AI prompts and responses, plus a comparison with HermiT |
| `count_solutions.py` | Brute-force count of consistent arrangements per stage, used in the comparison |

The files use Turtle syntax and open directly in Protégé.

## Encoding

- **Categories:** `House`, `Person`, `Color`, `Beverage`, `Pet` and `CigaretteBrand`. Each is closed with `owl:oneOf` over its five named individuals, the categories are pairwise disjoint, and each category's members are `owl:AllDifferent`.
- **One-to-one constraints:** every house has exactly one value per category (`qualifiedCardinality 1`). Each pair of properties (`livesIn`/`hasResident`, `colorOf`/`hasColor`, `drunkIn`/`hasDrink`, `keptIn`/`hasPet`, `smokedIn`/`hasSmoke`) are inverses of each other, and every one of them is both functional and inverse-functional.
- **Row order:** `nextTo` is symmetric and irreflexive. `immediatelyRightOf` is functional, inverse-functional, asymmetric, and irreflexive, with House *n+1* `immediatelyRightOf` House *n*. Both are closed with `allValuesFrom {…}` on each house, because otherwise the open-world assumption would allow unstated neighbours.
- **Clues are restrictions, not guessed facts.** For example, clue 2 is `Englishman ∈ livesIn some (hasColor value Red)`. Only clues 9 and 10 name a specific house, so only they are plain assertions. None of the clues encodes the conclusion.

## HermiT results per stage

| Stage | Consistent | New facts inferred about houses | `Person and livesIn some (hasPet value Zebra)` |
|---|---|---|---|
| 1 (clues 1–5) | Yes | None | No instances |
| 2 (clues 1–8) | Yes | None | No instances |
| 3 (clues 1–11) | Yes | None beyond the two asserted facts (Norwegian → House 1, milk → House 3) | No instances |
| 4 (clues 1–15) | Yes | The full arrangement (below) | **Japanese** |

Stage 4 inferred arrangement (everything except "Norwegian in House 1" and "milk in House 3" is inferred):

| House | Resident | Colour | Drink | Pet | Smoke |
|---|---|---|---|---|---|
| 1 | Norwegian | Yellow | Water | Fox | Kools |
| 2 | Ukrainian | Blue | Tea | Horse | Chesterfields |
| 3 | Englishman | Red | Milk | Snails | Old Gold |
| 4 | Spaniard | Ivory | Orange juice | Dog | Lucky Strike |
| 5 | Japanese | Green | Coffee | Zebra | Parliaments |

The reasoner's answer agrees with the brute-force count, which finds exactly one consistent arrangement at stage 4.

## Deductive vs. abductive

For stages 1–3, HermiT entails no zebra owner, and the brute-force count confirms that the four possible candidates are almost evenly split. The AI model still offered a pick at every stage. Its stage 3 justification sounded plausible but pointed to the candidate that was actually least likely. At stage 4 the AI model and HermiT agree, because the clues now determine the answer. See `ai-log.md` for details and the contamination caveat.

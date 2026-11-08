# TEST_LOG

What was run, what came out, and whether it matched. All data is synthetic practice data.
Each result below is copied from a real run of the script named, on `main` at commit `ba960ca` (merge of PR #2), on 2026-11-07.

## Anchor: Day 15 verified totals

Every later day must reproduce these exactly. Formula: `hourly_rate × hours + stipend`.

| Rank | City | Working | Weekly total |
|---|---|---|---|
| 1 | Boston | 35 × 40 + 2,500 | **$3,900.00** |
| 2 | Burlington | 42 × 36 + 1,900 | **$3,412.00** |
| 3 | Cleveland | 39.53 × 36 + 1,700 | **$3,123.08** |
| | **Grand total** | 3,900 + 3,412 + 3,123.08 | **$10,435.08** |

`python3 day15.py`: all three rows printed `OK` (stored = recomputed after the CSV read-back), and the grand total was $10,435.08. **PASS**

## Day 16: error handling (`python3 day16.py`)

| Test | Input | Expected | Actual | Result |
|---|---|---|---|---|
| 1 Good files | `ranked_offers.txt`, `offers.csv` as written | Same as anchor | 3 of 3 rows used, $10,435.08 | PASS |
| 2 Missing file | `no_such_ranking.txt`, `no_such_offers.csv` | Friendly message, fall back to memory, no crash | Both messages shown, $10,435.08 from memory | PASS |
| 3 Bad row | Burlington total = `"three thousand four hundred"` | Skip and name Burlington; 3,900 + 3,123.08 | Skipped Burlington (`ValueError`), $7,023.08, 2 of 3 rows | PASS |
| 4 Missing column | Cleveland row has 5 values | Skip and name Cleveland; 3,900 + 3,412 | `expected 6 values, got 5`, $7,312.00, 2 of 3 rows | PASS |
| Extra checks (scratch file, not in repo) | Blank line; 7-value row | Both skipped | Both skipped, rest totalled | PASS |

## Day 17: module + dates (`python3 day17.py`)

| Check | Expected | Actual | Result |
|---|---|---|---|
| Imports `rank_offers` from `offer_ranking.py` | Runs, no traceback | Runs, no traceback | PASS |
| Ranking order | Boston → Burlington → Cleveland | Boston → Burlington → Cleveland | PASS |
| Totals vs anchor | $3,900.00 / $3,412.00 / $3,123.08 / $10,435.08 | Same | PASS |
| Boston length | 2027-01-04 to 2027-04-04, both days counted | 91 days (13 weeks 0 days) | PASS |
| Burlington length | 2027-02-01 to 2027-03-28 | 56 days (8 weeks 0 days) | PASS |
| Cleveland length | 2027-01-11 to 2027-04-07 | 87 days (12 weeks 3 days) | PASS |
| Bad date | Denver `2027-02-30` | `skipped Denver: bad date (day is out of range for month)` | PASS |

## `rank_offers` edge cases (run directly in Python)

| Input | Actual | Matches SPEC |
|---|---|---|
| `rank_offers([])` | `[]` | Yes |
| `rank_by="city"` | Prints `unknown rank_by: city`, returns `[]` | Yes |
| Two offers tied at $100 (A, then B) | Order A, B | Yes |
| Offer missing `stipend` | `KeyError: 'stipend'` (not handled) | Yes, documented as open |
| `hourly_rate` = `"42"` (text) | `TypeError` (not handled) | Yes, documented as open |

## Planted-bug check (throwaway branch `day18-bug-ascending`: never pushed or merged, deleted after the check)

On that branch only, `reverse=True` was changed to `reverse=False` in `offer_ranking.py`.

| Check | Result on the bug branch |
|---|---|
| Totals per city | Unchanged: $3,900.00 / $3,412.00 / $3,123.08 |
| Grand total | Unchanged: $10,435.08 |
| Order | **Wrong:** Cleveland ranked 1st, Boston 3rd |

**Lesson:** the totals anchor alone would *pass* this bug. Always check the order as well (SPEC done criterion 2).

# SPEC: `offer_ranking.py`

All offers in this repo are synthetic practice data (made-up cities, rates and dates). No real contracts, names or personal data.

## Purpose

Rank contract offers from best to worst, so every day's script uses **one** shared, checked version of the ranking instead of a copy-pasted one. It works out each offer's weekly total in exactly one place.

## Function

```python
rank_offers(offer_list, rank_by="weekly_total")
```

### Inputs

| Input | Type | Rule |
|---|---|---|
| `offer_list` | list of dicts | Each dict must have `hourly_rate`, `hours`, `stipend` as **numbers** (int or float). Other keys (`city`, `start`, `end`, …) are carried along untouched. |
| `rank_by` | text | `"weekly_total"` (default) or `"hourly_rate"`. Anything else is rejected. |

### Outputs

- Returns a **new list**, sorted **highest first** (`reverse=True`) by `rank_by`.
- **Side effect:** adds or overwrites `weekly_total` on every offer dict passed in:
  `weekly_total = hourly_rate × hours + stipend`.
  The caller's own dicts change, but the caller's list keeps its original order.
- Prints nothing on success. Importing the module prints nothing.

### Ties

Python's `sorted` is *stable*, so offers with equal values keep the order they came in. For example, A ($100) listed before B ($100) stays A, B.

## Edge cases

The **boundary** matters here: `rank_offers` only works on offers already in memory. File, CSV-row and date problems are handled *before* the offers reach it, by the calling script.

| Case | Handled where | Behaviour (verified) |
|---|---|---|
| Empty list `[]` | `rank_offers` | Returns `[]`. No crash. |
| Unknown `rank_by` (e.g. `"city"`) | `rank_offers` | Prints `unknown rank_by: city`, returns `[]`. |
| Offer missing a key (e.g. no `stipend`) | **Not handled** | Crashes with `KeyError: 'stipend'`. The caller must supply complete offers. |
| Rate given as text (`"42"`) | **Not handled** | Crashes with `TypeError`. (Gotcha: `"42" * 36` repeats the text 36 times; the `+ stipend` is what finally fails.) Convert with `float()` first, as on Day 15. |
| Missing file (`ranked_offers.txt` / `offers.csv`) | `day16.py` (`show_text_ranking`, `grand_total_from_csv`) | Friendly message, then falls back to the offers in memory. Grand total is still $10,435.08. |
| Bad value in a CSV row (`"three thousand four hundred"`) | `day16.py` (`grand_total_from_csv`) | `ValueError` caught. That row is skipped and named, and the good rows still total. |
| Missing column (5 values instead of 6), extra column, blank line | `day16.py` (`grand_total_from_csv`) | `len(row) != len(header)` is checked before unpacking. The row is skipped and named. |
| Bad date (`2027-02-30`) | `day17.py` (`contract_length`) | `date.fromisoformat` raises `ValueError`, which is caught. The offer is reported as skipped. |

## Done criteria

1. `python3 day17.py` runs with no traceback and imports `rank_offers` from `offer_ranking.py`.
2. The ranking order by weekly total is **Boston → Burlington → Cleveland**.
3. The totals match the Day 15 anchor exactly: Boston **$3,900.00**, Burlington **$3,412.00**, Cleveland **$3,123.08**, grand total **$10,435.08**.
4. `rank_offers([])` returns `[]`, and an unknown `rank_by` returns `[]` with a message.
5. The Day 16 tests 1–4 and the Day 17 bad-date test give the results recorded in [TEST_LOG.md](TEST_LOG.md).

> Note: matching totals is **not enough on its own**. A wrong sort direction gives the *same* totals and grand total in the *wrong order*, so criterion 2 has to be checked separately.

## Out of scope (open)

- No checking that offer values are numbers or that keys exist. A bad offer crashes (see above).
- Contract length is not used in any pay math yet (e.g. total contract pay = weekly total × weeks).

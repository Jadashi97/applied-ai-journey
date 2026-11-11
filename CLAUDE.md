# CLAUDE.md

Guidance for Claude when working in this repo. Read this first every session, and update the **Progress log** at the end of each day's work.

## What this project is

A daily, hands-on learning journal for an **applied AI journey** (see [README.md](README.md) for the full why). It starts with Python fundamentals and will grow toward working with AI tools, APIs, and small apps. The goal is understanding and good judgment, not just finished code.

## How to help me (review mode)

- **Claude writes the code; I review it.** I don't write code myself, so don't ask me to type or retype it. My skill is reading code and understanding what it does and whether it's right.
- **After writing code, run it and walk me through it.** Show the real output and explain what each part does and *why*, in short, plain language.
- **Show me how to check it.** Point out what to verify (e.g. does the math match a number I already know, like the Stability split) and where code like this usually goes wrong.
- **One new concept at a time.** Don't introduce functions, classes, or libraries before the day's lesson reaches them.
- **Point out mistakes clearly**, e.g. double-counting values, duplicated lines, off-by-one indexes — and say how to spot them when reviewing.
- **Suggest a next step** at the end of a session that builds review skill (what to read, check, or learn next) — not a coding exercise.
- When we start AI work: always mention cost, privacy, and accuracy limits of the tool, and when a human should check the output.

## Repo structure

- One file per day: `dayN.py` (e.g. `day1.py`, `day2.py`, `day3.py`). Reflection days use `dayN.md`.
- Flat structure for now. When a project grows beyond one file, give it its own folder (e.g. `projects/<name>/`) with a short README.
- No dependencies yet — plain Python 3 standard library.

## Coding conventions (match these)

- Each exercise starts with a numbered comment describing the task: `#1 example ...`
- Use real-life context in examples (pay, contracts, states, facilities) — it makes the concepts stick.
- `snake_case` variable names that describe the value (`weekly_pay`, `filing_states`).
- Print results with f-strings, labeled: `print(f"weekly_pay: ${weekly_pay}")`.
- Short inline comments to explain a non-obvious choice (e.g. why a value isn't added twice).
- Keep each example tiny and runnable on its own top-to-bottom.

## Running code

```bash
python3 day5.py
```

## Git workflow

Never commit straight to `main`. Every change goes through a branch and a pull request, so it gets read before it lands. (Why: see [DECISIONS.md](DECISIONS.md) #5.)

1. **Branch from the latest `main`** for each day's work, e.g. `day19-docs`. Start a fresh branch after a PR is merged; never reuse a merged PR.
2. **Commit** on that branch. Message format: `Day N: <topic> — <what>` (e.g. `Day 5: lists and loops — examples`). Fixes to an earlier day: `Day N: fix <what>`.
3. **Push** the branch and **open a PR** into `main`.
4. **Review before merging:**
   - Run the script and check it against the Day 15 anchor: the totals (Boston $3,900.00, Burlington $3,412.00, Cleveland $3,123.08, grand total $10,435.08) **and** the order (Boston → Burlington → Cleveland). Totals alone don't catch a sort bug.
   - Try one bad input on purpose.
   - Read the diff until every changed line can be explained. If not, ask for an explanation and don't merge yet.
   - Scan for secrets and real personal data. All offer data stays synthetic.
5. **Merge** only after all of the above, and only when I say so.
6. Update the **Progress log** below as part of the day's PR.

## Progress log

Add a line each day: date, topic, what I learned, what was hard.

| Day | File | Topic | Notes |
|-----|------|-------|-------|
| 1 | `day1.py` | First Python | Variables, multiplication, f-string printing (contract pay). |
| 2 | `day2.py` | Variables, numbers, printing | Chained pay calculations. Lesson: don't subtract/add the same amount twice (loan double-counting fix). |
| 3 | `day3.py` | Strings | `split()`, slicing `[-2:]`, `[:5]`; cleaning with `strip()`, `title()`, `lower()`, `replace()` (chained); f-string number formatting `:,.2f`; `len()`. |
| 4 | `day4.py` | Input + tip calculator | `input()` returns text → convert with `float()` / `int()`; percent math; split a total; `:,.2f` formatting. |
| 5 | `day5.py` | Lists and loops | Indexing, negative index, `append()`, `max()`, `len()`, index assignment, `for` loops. |
| 6 | `day6.py` | Pay calculator | Reused Day 4's input → math → print shape. Checked against the Stability split: 36 × $39.53 + $1,673 = $3,096.08. |
| 7 | `day7.md` | Reflection | 5 lines on what clicked and what didn't. Decided: Claude writes the code, I review it. |
| 8 | `day8.py` | Dictionaries | Labelled boxes vs numbered boxes: `d["key"]`, update/add a key, `.keys()` / `.values()`, `in` to check a key, `.get(key, fallback)` to avoid a crash. |
| 9 | `day9.py` | For-loops | Loop over lists and a list of dicts; per-item math inside the loop; running total starts at 0 before the loop, prints after it; `range(1, 6)` stops before 6; `.items()` for label + value. Checked: Cleveland = $3,096.08. |
| 10 | `day10.py` | While-loops + if/elif/else | `while` needs a line that changes the counter or it never stops; `%` for even/odd; `if`/`elif`/`else` checks top-down, first match wins; `and` needs both true. Gotcha: "add while under $10,000" ended at $11,280 because the check happened *before* adding; fixed (my idea) with an `if` that checks `total + next <= 10000` first and `break` to stop → $7,520. |
| 11–13 | `day13.py` | Best offer → function → flexible function | Track "best so far" and update only when beaten (`>`, so a tie keeps the first). `def` + `return` hands back the winner instead of printing. Default argument `rank_by="weekly_total"`. Empty list returns `None`; check `is None` before using it. Checked: Boston wins on total ($3,900 at 40 hours), Burlington on rate ($42), Cleveland wins when its stipend goes to $3,000. |
| 14 | `day14.py` | Ranking all offers | `sorted(list, key=..., reverse=True)` returns a new ordered list; `lambda offer: offer[rank_by]` is a one-line "what to sort on". Weekly total computed in one place and stored on each offer; one print function for the layout. Empty list → empty ranking (`if not ranked`). Checked: total order Boston $3,900 > Burlington $3,412 > Cleveland $3,123.08; rate order Burlington > Cleveland > Boston; list 2 Cleveland 1st at $4,423.08. |
| 15 | `day15.py` | Files | `with open(name, "w")` writes (and wipes any old copy); `write()` needs `"\n"` for a new line; the file is saved when the `with` block ends; `open(name, "r")` + `.read()` reads it back. One `file_name` variable for both steps. Checked: `ranked_offers.txt` matches day14 — Boston $3,900.00, Burlington $3,412.00, Cleveland $3,123.08. Then CSV: `csv.writer` + header row, `newline=""`; `csv.reader` gives every value back as **text**, so `float()` before math (`"3900" + "3412"` = `"39003412"`). Recomputed each total from the read-back: all match; grand total $10,435.08. Output files are in `.gitignore`. |
| 16 | `day16.py` | Error handling | `try`/`except` with one **specific** error each: `FileNotFoundError` (missing file), `ValueError` (`float("forty two")`), `KeyError` (missing dict key); `as error` shows Python's own message. Read a traceback bottom-up: last line = what kind of error, line above = where. Applied to the contract tool: missing file → friendly message + fall back to the offers in memory; `try` *inside* the loop + `continue` skips one bad CSV row and keeps going. Checked: good files $10,435.08 (same as day15); missing files $10,435.08 from memory; bad Burlington row skipped → Boston $3,900 + Cleveland $3,123.08 = $7,023.08. Fixed later: a row with a missing column used to crash (the unpack sat outside the `try`); now `len(row) != len(header)` is checked first → skipped and noted (test 4: Cleveland short row → Boston + Burlington = $7,312.00; blank and extra-column rows also skipped). |
| 17 | `day17.py` + `offer_ranking.py` | Modules + dates | Moved `rank_offers` into its own module `offer_ranking.py` (a module = a `.py` file you import; it only defines, never prints). `from offer_ranking import rank_offers` in day17. `from datetime import date`; `date.fromisoformat("2027-01-04")` turns text into a real date; end − start gives `.days` *between* → `+1` to count both first and last day (off-by-one). `//` = whole weeks, `%` = leftover days. Bad date (`2027-02-30`) → `ValueError`, caught as on Day 16. Checked: Boston $3,900.00 / 91 days (13 wks), Burlington $3,412.00 / 56 days (8 wks), Cleveland $3,123.08 / 87 days (12 wks 3 days); grand total $10,435.08 = day15. `__pycache__/` added to `.gitignore`. |
| 18 | `SPEC.md`, `TEST_LOG.md` | Review: spec, test log, planted bug | Wrote a spec for `rank_offers` (inputs, outputs, edge cases, done criteria) and a test log of real results. Learned where each edge case is handled: the module handles only empty list + unknown `rank_by`; files/rows in `day16.py`, dates in `day17.py`. Not handled: missing key → `KeyError`, rate as text → `TypeError` (`"42" * 36` repeats the text). Planted bug `reverse=False`: every total and $10,435.08 still matched, only the **order** was wrong → check order separately. Bug branch never pushed, deleted. PR #3. |
| 19 | `README.md`, `DECISIONS.md` | Docs + decisions | README documents the contract tool (run, demo output, edge cases, honest limits) under the original intro. DECISIONS.md records the Days 14–18 choices: what was chosen, why, what was rejected. Git workflow above changed from "commit on `main`" to branch → PR → review → merge. Checked: day17.py on `main` = anchor totals and order. PR #4. |
| 21 | `day21.py` | SQL with `sqlite3` | A database is a file of tables; `sqlite3.connect("offers.db")` creates it, the cursor runs SQL. `CREATE TABLE` with TEXT/REAL/INTEGER; `INSERT` with `?` placeholders (never f-strings: a quote mark like O'Hare breaks them); `commit()` saves. `ORDER BY ... DESC` = `sorted(reverse=True)`, `WHERE` = an `if`, SQL compares with one `=`, `SUM` = the running total. Weekly total still worked out once, by `rank_offers`. Gotchas: without `DROP TABLE IF EXISTS` a second run doubles every row (grand total $20,870.16, tested); `SUM` of no rows is `None`, not 0. Checked: Boston $3,900.00 → Burlington $3,412.00 → Cleveland $3,123.08, SUM $10,435.08; `> 10000` prints "no offers found". `offers.db` added to `.gitignore`. PR #5. |
| 22 | `day22.py` | SQL: WHERE, AND/OR, BETWEEN, ORDER BY, LIMIT | Rebuilt `offers.db` with a `state` column; read the 3 offers from `offers.csv` (text → `float()`/`int()`), state and dates added from a city lookup. If `offers.csv` is missing (it's git-ignored), falls back to offers in memory. **Every value is a `?`** with values passed separately, even `LIMIT ?`; only column names/SQL words are written in. AND narrows (both true → Burlington only), OR widens (either true → all 3). `BETWEEN 3100 AND 3500` includes both ends; `ASC` = smallest first (Cleveland, Burlington). `ORDER BY hourly_rate DESC LIMIT 1` → Burlington $42 (a different winner from the total ranking). `WHERE state = 'TX'` → "no offers found". Checked: order Boston → Burlington → Cleveland, SUM $10,435.08 with and without `offers.csv`; second run still 3 rows. |

## Roadmap (flexible)

1. Python basics: variables → strings → lists/loops → conditionals → functions → dicts → files
2. Small scripts that solve real tasks (e.g. pay/contract calculator)
3. Working with data (CSV, JSON)
4. Calling an AI API (Claude) from Python; prompting basics
5. Evaluating AI output: accuracy, errors, when human review is needed
6. Build a small applied AI app end to end

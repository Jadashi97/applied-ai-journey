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

- Commit at the end of each day on `main`.
- Message format: `Day N: <topic> — <what>` (e.g. `Day 5: lists and loops — examples`).
- Fixes to an earlier day: `Day N: fix <what>`.

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

## Roadmap (flexible)

1. Python basics: variables → strings → lists/loops → conditionals → functions → dicts → files
2. Small scripts that solve real tasks (e.g. pay/contract calculator)
3. Working with data (CSV, JSON)
4. Calling an AI API (Claude) from Python; prompting basics
5. Evaluating AI output: accuracy, errors, when human review is needed
6. Build a small applied AI app end to end

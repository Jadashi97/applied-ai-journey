# CLAUDE.md

Guidance for Claude when working in this repo. Read this first every session, and update the **Progress log** at the end of each day's work.

## What this project is

A daily, hands-on learning journal for an **applied AI journey** (see [README.md](README.md) for the full why). It starts with Python fundamentals and will grow toward working with AI tools, APIs, and small apps. The goal is understanding and good judgment, not just finished code.

## How to help me (learning mode)

- **I'm a beginner learning by doing.** Explain *why*, not just *what*. Keep explanations short and plain.
- **Let me write the code first.** When I'm doing exercises, give hints or point out the bug before handing over a full solution — unless I ask for the answer.
- **One new concept at a time.** Don't introduce functions, classes, or libraries before the day's lesson reaches them.
- **Point out mistakes clearly**, e.g. double-counting values, duplicated lines, off-by-one indexes — and say how to spot them next time.
- **Suggest a next step** at the end of a session (what to practice or learn tomorrow).
- When we start AI work: always mention cost, privacy, and accuracy limits of the tool, and when a human should check the output.

## Repo structure

- One file per day: `dayN.py` (e.g. `day2.py`, `day3.py`, `day5.py`). `hello.py` is Day 1.
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
| 1 | `hello.py` | First Python | Variables, multiplication, f-string printing (contract pay). |
| 2 | `day2.py` | Variables, numbers, printing | Chained pay calculations. Lesson: don't subtract/add the same amount twice (loan double-counting fix). |
| 3 | `day3.py` | Strings | `split()`, slicing `[-2:]`, `[:5]`; cleaning with `strip()`, `title()`, `lower()`, `replace()` (chained); f-string number formatting `:,.2f`; `len()`. |
| 4 | `day4.py` | Input + tip calculator | `input()` returns text → convert with `float()` / `int()`; percent math; split a total; `:,.2f` formatting. |
| 5 | `day5.py` | Lists and loops | Indexing, negative index, `append()`, `max()`, `len()`, index assignment, `for` loops. |

## Roadmap (flexible)

1. Python basics: variables → strings → lists/loops → conditionals → functions → dicts → files
2. Small scripts that solve real tasks (e.g. pay/contract calculator)
3. Working with data (CSV, JSON)
4. Calling an AI API (Claude) from Python; prompting basics
5. Evaluating AI output: accuracy, errors, when human review is needed
6. Build a small applied AI app end to end

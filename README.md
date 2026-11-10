# Applied AI Journey

## Project purpose

This repository is a home for a hands-on journey into applied artificial intelligence. Its purpose is to turn curiosity about AI into practical understanding: to explore how AI systems and tools work, try them on real tasks, and learn from the results. Instead of keeping experiments and insights scattered, this project brings them together so progress can be reviewed, improved, and built upon.

## Why I started this project

AI is becoming part of how people research, communicate, create, and solve problems. Understanding it requires more than knowing that the tools exist. I want to develop the judgment to choose appropriate tools, use them effectively, recognize their limitations, and evaluate the quality of their results.

The most useful way for me to develop that judgment is through practice. Small experiments and projects make abstract ideas concrete: they reveal what a tool can do, where it struggles, and what skills or knowledge I need to develop next. Recording that work also makes the learning cumulative: each new effort can benefit from the questions, decisions, and lessons captured in earlier ones.

## What I am working toward

- Build a practical foundation in applied AI concepts, methods, and tools.
- Explore AI-assisted workflows and identify situations where they provide genuine value.
- Learn by making experiments and projects, not just by collecting information.
- Improve my ability to assess outputs, notice errors and uncertainty, and decide when human review is needed.
- Consider privacy, safety, fairness, and other responsible-use questions as part of applying AI.
- Keep useful notes on goals, approaches, outcomes, challenges, and lessons learned.
- Develop a body of work that shows my progress and provides a foundation for future ideas.

## How I plan to use this repository

Each addition should serve the learning process: explain an idea, record an experiment, demonstrate an application, or reflect on a result. Where useful, I can describe the problem I was exploring, the approach and tools I tried, what happened, and what I would change next time. Unsuccessful or unexpected outcomes are worth recording when they clarify a limitation or suggest a better direction.

I will approach the work incrementally, choosing focused questions and building on what I learn rather than trying to cover all of AI at once. The project's topics and structure can change as my interests and skills develop. The goal is ongoing, thoughtful progress—not to imply that I have already mastered the field. Ultimately, I want this repository to help me become more capable and discerning in applying AI, while making the reasoning and learning behind that progress clear to my future self and to others.

## Project so far: contract offer tool

A small Python tool, built one lesson at a time (Days 14–18), that compares travel-contract offers. All offers, cities, rates and dates in this repo are **synthetic practice data**. They are not real contracts and contain no personal data.

### What it does

- Works out each offer's **weekly total**: `hourly_rate × hours + stipend`.
- **Ranks** the offers from best to worst by weekly total (or by hourly rate, if asked).
- Reads each offer's start and end **dates** and shows the contract length in days and weeks.
- Adds up a **grand total** of all weekly totals.

The ranking itself lives in one shared module, [`offer_ranking.py`](offer_ranking.py) (function `rank_offers`). [`day17.py`](day17.py) imports it and adds the dates.

### How to run it

Plain Python 3, nothing to install:

```bash
python3 day17.py
```

### Demo output

Copied from a real run on `main`:

```
ranked by weekly total, with contract length:
  1. Boston: weekly total $3,900.00 | 2027-01-04 to 2027-04-04 = 91 days (13 weeks 0 days)
  2. Burlington: weekly total $3,412.00 | 2027-02-01 to 2027-03-28 = 56 days (8 weeks 0 days)
  3. Cleveland: weekly total $3,123.08 | 2027-01-11 to 2027-04-07 = 87 days (12 weeks 3 days)
grand_total of all weekly totals: $10,435.08

skipped Denver: bad date (day is out of range for month)
```

These are the **Day 15 anchor totals** that every later version must reproduce exactly: Boston **$3,900.00**, Burlington **$3,412.00**, Cleveland **$3,123.08**, grand total **$10,435.08**. The working for each total is in [TEST_LOG.md](TEST_LOG.md).

### Edge cases handled

| Problem | What happens | Where |
|---|---|---|
| Empty list of offers | Returns an empty ranking; no crash | `offer_ranking.py` |
| Unknown ranking choice (e.g. `"city"`) | Prints a message, returns an empty ranking | `offer_ranking.py` |
| Missing file (`ranked_offers.txt` / `offers.csv`) | Friendly message, then uses the offers in memory | `day16.py` |
| A CSV value that isn't a number | That row is skipped and named; the good rows still total | `day16.py` |
| A CSV row with a missing or extra column, or a blank line | That row is skipped and named | `day16.py` |
| A date that doesn't exist (Feb 30) | That offer is skipped with a message | `day17.py` |

When rows are skipped, the total says so (for example "2 of 3 rows used"), so a partial total can't be mistaken for a full one.

### Honest limits

- **Missing key → `KeyError`.** An offer without `hourly_rate`, `hours` or `stipend` crashes the ranking. Nothing checks for this yet.
- **Rate as text → `TypeError`.** A rate written as `"42"` instead of `42` crashes. (Gotcha: `"42" * 36` doesn't fail; it repeats the text 36 times. The crash comes one step later, at `+ stipend`.) Values read from a file must be converted with `float()` first.
- **Totals alone don't catch a sort bug.** On Day 18, flipping the sort to lowest-first left every total and the grand total unchanged, with only the order wrong. So the order (Boston → Burlington → Cleveland) is **checked separately** from the totals.
- **The ranking changes the offers you pass in.** It adds a `weekly_total` value to each one.
- **Contract length isn't used in pay math yet.** Total pay over a whole contract is not calculated.
- **No automated tests in the repo yet.** Checks are run by hand and recorded in [TEST_LOG.md](TEST_LOG.md).

### More detail

- [SPEC.md](SPEC.md): what `rank_offers` takes, returns, and promises.
- [TEST_LOG.md](TEST_LOG.md): every check that was run, with real results.
- [DECISIONS.md](DECISIONS.md): the choices made along the way, and what was rejected.

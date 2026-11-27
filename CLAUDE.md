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
- Dependencies: Days 1–23 use only the plain Python 3 standard library. From Day 24, `pandas` is needed, from Day 25 `requests`, from Day 26 `anthropic` (only for a real LLM call), and from Day 28 `chromadb` (Day 30 also uses its built-in local embedding model, downloaded once, ~80 MB); all are listed (pinned) in [requirements.txt](requirements.txt). Add any new library there in the same PR that first uses it.

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

For Day 24 and later, install the libraries first (once):

```bash
pip install -r requirements.txt
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
| 23 | `day23.py` | SQL: JOIN, GROUP BY, HAVING | Second table `state_pay` (MA/VT/OH/NH avg + max pay, license; Vivian figures as given, not re-checked). JOIN matches rows on the shared `state` column: INNER keeps only matches (3 rows, NH dropped), LEFT keeps every left row (NH shows "no offer", its offer columns are `None`). `AS difference` names a computed column so `ORDER BY` can use it → Boston +$879 > Cleveland +$573.08 > Burlington +$171 (a different order from the total ranking). `GROUP BY` = one row per value: 36 hrs sum $6,535.08 / avg $3,267.54, 40 hrs $3,900. `HAVING` filters groups *after* the math, `WHERE` filters rows before → `HAVING AVG > 3400` keeps only 40 hrs, even though Burlington alone is $3,412. No f-strings in any SQL; every value is a `?`. Gotcha (tested): a duplicate MA row in `state_pay` makes the INNER JOIN return 4 rows and sum $14,335.08 (Boston counted twice). Checked: SUM $10,435.08; Boston → Burlington → Cleveland in (1); second run still 3 + 4 rows. |
| 24 | `day24.py`, `offers_messy.csv` | pandas: cleaning messy data | First outside library (`pandas`, pinned in `requirements.txt`). A DataFrame is a table with named columns. Messy file: 7 synthetic rows = 3 good + exact Boston duplicate, Austin rate `"forty"`, `"  Burlington  "` (a duplicate once stripped), Denver blank stipend. Steps: `str.strip()` → `pd.to_numeric(errors="coerce")` (bad value → NaN, no crash) → `dropna` (dropped, not filled with 0) → `drop_duplicates` → `weekly_total` in one line for every row → `to_csv`. **Order matters (tested):** strip after dedup keeps both Burlingtons → $13,847.08; the anchor caught it, but the `rank_offers` cross-check still said True (it checks the math, not which rows belong). Checked: kept 3 of 7, Boston $3,900.00 → Burlington $3,412.00 → Cleveland $3,123.08, grand total $10,435.08. PR #8. |
| 25 | `day25.py`, `api_summary.json`, `.env.example` | Calling a web API with `requests` | Second outside library (`requests`, pinned). `requests.get(url, timeout=10)`: a timeout stops it waiting forever. Catch `Timeout` and `ConnectionError` separately; check `status_code == 200` before reading (404 = not found). `response.json()` turns JSON into dicts; the city is nested: `user["address"]["city"]`. Save `api_summary.json` **only on success**, so a failed run can't overwrite good data. Keys go in `.env` (git-ignored, never committed); `.env.example` holds only `API_KEY=your_key_here`. JSONPlaceholder users are made-up sample data. Bug found in my own code: the message typed "10 seconds" separately from `timeout=10` → one `timeout_seconds` variable. Checked: two runs both Leanne Graham / Gwenborough / 200, saved files identical; 404, 0.001s timeout and a fake host each print a clear message and save nothing. The cloud session needed `jsonplaceholder.typicode.com` allowed (owner approved a personal environment). PR #11. |
| 26 | `day26.py`, `llm_ranking.json`, `.env.example` | First LLM call (Claude) with a validator | Python recomputes the totals first: they are the source of truth. System prompt = rules (JSON only, exact keys `ranking`/`best_city`/`reason`, highest first); user prompt = the data. `call_llm()` reads `LLM_API_KEY` from `.env` (never in code); no key → `log: no key found, using stub`. The stub is typed from the anchor by hand, **not** built from the recomputed totals, or the check would always pass. With a key: official `anthropic` library, `claude-opus-5-5`, 30 s timeout, no retries, effort low, refusal fallback on. `validate()` rejects unless keys, number types, every total to the cent, **order** and `best_city` are right; nothing saved unless all pass; `source` field says stub or model. Checked: anchor match, best_city Boston; 9 bad replies rejected; 6 broken replies end to end (cut off, code fence, prose, empty, a list, Boston $3,990) → clear message, no crash, no file; fake key → 401; fake local server: good saved, wrong total rejected, slow → timeout. **No real call made yet.** AI limits: cost per token, prompt goes to the provider (synthetic data only), the `reason` sentence still needs a human read. Open: a rejected run leaves an older good file in place and still exits 0. PR #13. |
| 27 | `day27.py`, `eval_results.json` | Structured output + first eval | One strict JSON Schema (`required`, `additionalProperties: false`) used twice: sent to the API as structured output and checked locally on every reply. A schema checks **shape**, not truth, so totals to the cent, order, `best_city` = top city and one-sentence `reason` are separate checks. Fixed Day 26's open points: a good reply goes to a `.tmp` file then `os.replace` (no half-written file); any rejection deletes the old `llm_ranking.json` and exits 1. Eval set of 5 hand-made replies (1 accept, 4 reject) → 5/5; it tests the **checker**, not the model. Checked: with the `best_city` check deleted, the eval dropped to 4/5 and exited 1. Gotcha: `echo $?` after a pipe shows the last command's code, not Python's. PR #15. |
| 28 | `day28.py`, `docs/`, `rag_eval.json` | RAG step 1: chunking + retrieval | 3 synthetic offer docs, each with its own total + one unique fact. Chunks of ~500 characters with ~50 overlap, metadata = file + chunk index. STUB embedding: key words hashed with `zlib.crc32` (Python's `hash()` changes per run). Stored in Chroma (telemetry off, no model attached, rebuilt each run so no duplicates). Confidence = the top chunk holds at least 50% of the question's key words; otherwise "I don't know". **Failure found:** the first cut split Cleveland's "$3,123.08 ... hourly pay" across 2 chunks → 2/3. Fixed by cutting at paragraph breaks, **not** by lowering the threshold. Checked: 3/3, Miami → "I don't know". Known limit: "completion bonus in Miami" gets a confident wrong hit (2 of 3 words match). `chromadb` added to `requirements.txt`. PR #16. |
| 29 | `day29.py`, `qa_eval.json` | RAG step 2: cited answers + answer checker | Loads Day 28's collection (doesn't rebuild it) and checks it: chunks still word for word in the docs, stored vectors = this file's copied `stub_embed`. Top 3 chunks, each labelled `[file.md, chunk N]`, go into the prompt with "answer ONLY from these, cite every fact". No key → a sentence quoted from the chunks; not confident → "I don't know" **without calling the model**. Checker: every citation must be a retrieved chunk, every number must be in the chunk it cites, a weekly total must equal the anchor. My mistakes caught: the grand total was first summed from the *expected* amounts (circular) → now read out of the answers; tied chunks came back in random order → fixed tie-break. Checked: 5/5, $10,435.08 from the answers; 9 bad answers rejected; a misquoted $3,990 → 4/5, exit 1. Fix (PR #19): after Day 30 rebuilt the collection, Day 29 crashed with a traceback; now it checks vector length first (`zip()` silently stops at the shorter list) and exits 1 with "run `python3 day28.py`". PR #17. |
| 30 | `day30.py`, `real_embeddings_eval.json` | Real embeddings vs the stub | Chroma's default model, all-MiniLM-L6-v2: 384 numbers per text, runs locally, free, no key; downloaded once, then works with the network cut. Only the embedding changed: chunking, confidence rule, answerer and checker are loaded from day28/day29 with `ast` (without running them). **Result: worse than the stub on our questions.** Retrieval 1/3 (stub 3/3), Q&A 3/5 (stub 5/5). Why: it judges meaning, and all 3 docs say "The weekly total is $…"; it rates the $3,900 and $3,412 sentences 0.957 alike, with only 0.007–0.019 between first and second place. **Safety held: 0 wrong answers;** both failures were "I don't know", because the word-coverage rule saw the number wasn't in the top chunk. Logged as findings, not hidden; the script exits 1 on purpose. Real-model limit: good at meaning, weak at exact numbers. PR #18. |

## Next up

- Nothing queued right now.

## Roadmap (flexible)

1. Python basics: variables → strings → lists/loops → conditionals → functions → dicts → files
2. Small scripts that solve real tasks (e.g. pay/contract calculator)
3. Working with data (CSV, JSON)
4. Calling an AI API (Claude) from Python; prompting basics
5. Evaluating AI output: accuracy, errors, when human review is needed
6. Build a small applied AI app end to end

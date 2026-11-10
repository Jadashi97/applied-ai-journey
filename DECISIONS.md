# DECISIONS

The choices made while building the contract offer tool (Days 14–18). For each one: what was chosen, why, and what was rejected. All offer data is synthetic.

---

## 1. Rank by weekly total by default, with hourly rate as an option (Day 14)

**Chosen:** `rank_offers` ranks by **weekly total** (`hourly_rate × hours + stipend`) unless asked to rank by `hourly_rate`. The weekly total is worked out in **one place** and stored on each offer, so every later step reads the same number.

**Why:** the weekly total is what actually gets paid. Hourly rate alone is misleading. Boston has the *lowest* rate ($35) but the *highest* weekly total ($3,900), because it has more hours and the biggest stipend. Ranking by rate puts Burlington first ($42) and Boston last.

**Rejected:**
- *Rate only.* It ignores the stipend and the hours, which together are most of the pay.
- *Working out the total separately in each place it's needed.* Copies drift apart. That's how a value gets double-counted, which was the Day 2 lesson.

---

## 2. Missing file → message, then fall back to the offers in memory (Day 16)

**Chosen:** if `ranked_offers.txt` or `offers.csv` is missing, catch **only** `FileNotFoundError`, say which file is missing, and carry on with the offers already in memory. The grand total is still $10,435.08.

**Why:** a missing output file isn't a reason to lose the whole ranking. The offers are already in memory, so the answer can still be given. The message keeps the problem visible.

**Rejected:**
- *Let it crash.* One missing file would stop everything.
- *Fall back silently.* You wouldn't know the file was missing.
- *Catch every error at once.* That hides real bugs, so a typo in the code would look the same as a missing file.

---

## 3. Skip bad rows and bad dates, name them, and keep going (Days 16–17)

**Chosen:**
- A CSV value that isn't a number (`"three thousand four hundred"`) → `ValueError` caught, row skipped and named.
- A row with the wrong number of values (missing column, extra column, blank line) → checked with `len(row) != len(header)` **before** unpacking, then skipped and named.
- A date that doesn't exist (`2027-02-30`) → `ValueError` caught, offer skipped and named.
- The total says how many rows it used (e.g. "2 of 3 rows used").

**Why:** one bad row shouldn't kill the whole ranking. The `try` sits **inside** the loop so the next row still runs. Naming the skipped row and showing "2 of 3" makes it clear that a total is partial.

**Rejected:**
- *Stop at the first bad row.* You lose all the good rows after it.
- *Treat a bad value as 0.* It would quietly make the total too low, with nothing to show it.
- *Guess the missing column.* A guessed number looks exactly like a real one.
- *Accept a row with extra columns.* An extra comma usually means values have shifted into the wrong columns.

**Related choice: counting contract days.** Contract length counts **both** the first and last day (`end − start + 1`), so Jan 4 to Jan 4 is 1 day. This is an assumption. If a real contract's end date is the day you leave, every length is one day too long.

---

## 4. Move the ranking into its own module (Day 17)

**Chosen:** `rank_offers` lives in `offer_ranking.py`. Day scripts import it (`from offer_ranking import rank_offers`) instead of carrying a copy. The module only defines the function; importing it prints nothing.

**Why:** one checked copy. Before this, Days 14, 15 and 16 each had their own copy, and a fix to one wouldn't reach the others. After the move, Day 17 was checked against the Day 15 anchor and matched exactly.

**Rejected:**
- *Keep copy-pasting the function into each day's file.* The copies drift apart.
- *Put it in a `projects/contract_tool/` folder now.* CLAUDE.md suggests this once a project grows past one file. It was left in the main folder to keep the import a single simple line. This is still open.

---

## 5. Work on a branch, open a PR, review, then merge (Days 16–18)

**Chosen:** every change goes on a branch and into a pull request. Before merging:
1. Run the script and check it against the anchor: the totals **and** the order.
2. Try one bad input on purpose.
3. Read the diff until every changed line can be explained. If it can't, ask for an explanation first.
4. Scan for secrets and real personal data.
5. Merge last.

**Why:** the person reviewing (me) doesn't write the code, so reviewing it *is* the skill being built. A PR shows exactly what changed, line by line. On Day 18, a planted bug (sorting lowest-first) passed every **total** check and was caught only by the **order** check. That's the reason the order is checked separately.

**Rejected:**
- *Committing straight to `main`.* There's no point where a change gets read before it lands. (CLAUDE.md still says "commit on `main`". That wording is out of date now that every change goes through a PR.)
- *Checking totals only.* The Day 18 bug passed every total check.
- *Merging the bug branch, or pushing it to GitHub.* The bug branch existed only to practise spotting the bug. It was never pushed, and it was deleted after the check.
- *Reusing a merged PR for follow-up work.* Each new piece of work gets a new PR.

import pandas as pd  # the repo's first outside library: pip install pandas (not part of plain Python)

from offer_ranking import rank_offers  # only used at the end, to cross-check pandas' totals

# offers_messy.csv: the 3 synthetic Day 15 offers plus 4 problem rows (all made up):
#   row 4  Boston       -> exact duplicate of row 1
#   row 5  Austin       -> hourly_rate written as text ("forty")
#   row 6  "  Burlington  " -> extra spaces; once stripped it's a duplicate of row 2
#   row 7  Denver       -> stipend left blank
messy_name = "offers_messy.csv"
clean_name = "offers_clean.csv"
number_columns = ["hourly_rate", "stipend", "hours"]

#1 example Day 24: read the CSV into a DataFrame -- pandas' table of rows and named columns.
offers = pd.read_csv(messy_name)
rows_read = len(offers)  # kept for the "kept N of M" line at the end
print(f"read {rows_read} rows from {messy_name}")

#2 example Day 24: strip spaces from every city name. This must come BEFORE removing duplicates:
# "  Burlington  " and "Burlington" are different text, so a duplicate check would keep both.
offers["city"] = offers["city"].str.strip()

#3 example Day 24: turn the number columns into real numbers. errors="coerce" means
# "if it can't be a number, mark it missing (NaN) instead of crashing" -- so "forty" becomes NaN.
for column in number_columns:
    offers[column] = pd.to_numeric(offers[column], errors="coerce")

#4 example Day 24: drop rows that can't be used -- any missing rate, stipend or hours.
# Dropped, not filled with 0: a guessed 0 would quietly make a total too low (DECISIONS #3).
unusable = offers[offers[number_columns].isna().any(axis=1)]
for row in unusable.itertuples():
    missing = [column for column in number_columns if pd.isna(getattr(row, column))]
    print(f"  dropped {row.city}: missing or not a number -> {missing}")
offers = offers.dropna(subset=number_columns)

#5 example Day 24: drop exact duplicate rows (every column the same). This runs AFTER the
# strip and the number conversion, so " Burlington " / "Burlington" and "35" / 35.0 all match.
duplicates = offers[offers.duplicated()]
for row in duplicates.itertuples():
    print(f"  dropped {row.city}: duplicate row")
offers = offers.drop_duplicates()

#6 example Day 24: work out weekly_total once per offer. One line does the math for every row:
# pandas multiplies the columns row by row, like the Day 9 loop without writing the loop.
offers["hours"] = offers["hours"].astype(int)  # 40.0 -> 40, now that no blanks are left
offers["weekly_total"] = offers["hourly_rate"] * offers["hours"] + offers["stipend"]

#7 example Day 24: best first, then save. index=False leaves out pandas' row numbers.
offers = offers.sort_values("weekly_total", ascending=False)
offers.to_csv(clean_name, index=False)
print(f"kept {len(offers)} of {rows_read} rows; saved to {clean_name}")

#8 example Day 24: print the clean rows and the grand total.
print("\nclean offers, ranked by weekly total:")
rank = 1
for row in offers.itertuples():
    print(f"  {rank}. {row.city}, {row.state}: ${row.hourly_rate:,.2f}/hr, ${row.stipend:,.0f} stipend, "
          f"{row.hours} hrs, weekly total ${row.weekly_total:,.2f}")
    rank = rank + 1
grand_total = offers["weekly_total"].sum()
print(f"grand_total: ${grand_total:,.2f}")  # should be $10,435.08 (Day 15 anchor)

#9 example Day 24: cross-check against the Day 17 module, the repo's one checked formula.
# Same three offers through rank_offers should give the same order and the same totals.
module_ranked = rank_offers(offers[["city", "hourly_rate", "stipend", "hours"]].to_dict("records"))
same_order = [offer["city"] for offer in module_ranked] == list(offers["city"])
same_totals = [round(offer["weekly_total"], 2) for offer in module_ranked] == list(offers["weekly_total"].round(2))
print(f"matches offer_ranking.py: order {same_order}, totals {same_totals}")

import csv  # part of plain Python, nothing to install

# ---------------------------------------------------------------------------
# Hour 1: try/except on small, safe examples.
# Pattern: put the risky line inside "try:"; if that exact kind of error happens,
# Python jumps to the matching "except" instead of crashing the whole program.
# Each except names ONE specific error, so a different mistake (like a typo) still shows up loudly.
# ---------------------------------------------------------------------------

#1 example Day 16: read a file that doesn't exist -> FileNotFoundError
missing_name = "offer_letter_that_does_not_exist.txt"
try:
    with open(missing_name, "r") as file:
        letter = file.read()
    print(f"letter: {letter}")  # only runs if the open worked
except FileNotFoundError:
    print(f"#1 couldn't find {missing_name} -- check the name or run the step that creates it")

#2 example Day 16: turn a rate written in words into a number -> ValueError
rate_text = "forty two"  # someone typed words instead of 42
try:
    hourly_rate = float(rate_text)
    print(f"hourly_rate: ${hourly_rate}")
except ValueError as error:  # "as error" keeps Python's own message so we can show it
    print(f"#2 '{rate_text}' isn't a number, so it can't be a rate (Python says: {error})")

#3 example Day 16: ask an offer for a key it doesn't have -> KeyError
offer = {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40}
try:
    overtime_rate = offer["overtime_rate"]  # Boston's offer never listed overtime
    print(f"overtime_rate: ${overtime_rate}")
except KeyError as error:
    print(f"#3 the {offer['city']} offer has no {error} key; known keys: {list(offer.keys())}")
# (Day 8's .get("overtime_rate", 0) also avoids the crash; try/except is the tool when
#  you can't give a sensible fallback value and want to say what went wrong instead.)


# ---------------------------------------------------------------------------
# Hour 2: the contract tool from day15, made to survive a missing file or one bad CSV row.
# ---------------------------------------------------------------------------

offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]


#4 example Day 16: same ranking as Day 14/15, copied here so this file runs on its own.
def rank_offers(offer_list, rank_by="weekly_total"):
    if rank_by not in ("weekly_total", "hourly_rate"):
        print(f"unknown rank_by: {rank_by}")
        return []
    for offer in offer_list:
        offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    return sorted(offer_list, key=lambda offer: offer[rank_by], reverse=True)


#5 example Day 16: write both files exactly like day15 (text file + CSV with a header row).
def write_files(ranked, text_name, csv_name):
    with open(text_name, "w") as file:
        rank = 1
        for offer in ranked:
            file.write(f"{rank}. {offer['city']}: ${offer['hourly_rate']}/hr, "
                       f"${offer['stipend']:,} stipend, {offer['hours']} hrs, "
                       f"weekly total ${offer['weekly_total']:,.2f}\n")
            rank = rank + 1
    with open(csv_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["rank", "city", "hourly_rate", "stipend", "hours", "weekly_total"])
        rank = 1
        for offer in ranked:
            writer.writerow([rank, offer["city"], offer["hourly_rate"], offer["stipend"],
                             offer["hours"], round(offer["weekly_total"], 2)])
            rank = rank + 1
    print(f"wrote {len(ranked)} offers to {text_name} and {csv_name}")


#6 example Day 16: read the text ranking back; if the file is missing, fall back to memory.
def show_text_ranking(text_name, ranked):
    try:
        with open(text_name, "r") as file:
            contents = file.read()
        print(f"contents of {text_name}:")
        print(contents, end="")  # the file already ends with "\n", so don't add another
    except FileNotFoundError:
        print(f"couldn't find {text_name} -- showing the ranking from memory instead:")
        rank = 1
        for offer in ranked:
            print(f"{rank}. {offer['city']}: weekly total ${offer['weekly_total']:,.2f}")
            rank = rank + 1


#7 example Day 16: add up the CSV totals; skip and note a bad row; fall back to memory if missing.
def grand_total_from_csv(csv_name, ranked):
    try:
        with open(csv_name, "r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)  # take the header row off first
            rows = list(reader)
    except FileNotFoundError:
        # no file to read, so use the totals already worked out in memory
        grand_total = 0
        for offer in ranked:
            grand_total = grand_total + offer["weekly_total"]
        print(f"couldn't find {csv_name} -- grand total from memory: ${grand_total:,.2f}")
        return grand_total

    grand_total = 0
    skipped = []  # cities whose row couldn't be read, so we can report them at the end
    for row in rows:
        rank, city, hourly_rate, stipend, hours, weekly_total = row
        # the try is INSIDE the loop: one bad row jumps to except, then the loop
        # carries on with the next row. A try around the whole loop would stop at the first bad row.
        try:
            stored_total = float(weekly_total)
            recomputed_total = float(hourly_rate) * float(hours) + float(stipend)
        except ValueError as error:
            print(f"  skipped {city}: {error}")
            skipped.append(city)
            continue  # go straight to the next row; this row adds nothing to the total
        if round(recomputed_total, 2) == round(stored_total, 2):
            print(f"  {city}: stored ${stored_total:,.2f} = recomputed ${recomputed_total:,.2f}  OK")
        else:
            print(f"  {city}: stored ${stored_total:,.2f} vs recomputed ${recomputed_total:,.2f}  MISMATCH")
        grand_total = grand_total + stored_total  # only good rows reach this line

    print(f"grand total from {csv_name}: ${grand_total:,.2f} "
          f"({len(rows) - len(skipped)} of {len(rows)} rows used)")
    if skipped:
        print(f"  note: skipped rows -> {skipped}; fix them in the file and run again")
    return grand_total


ranked = rank_offers(offers)

#8 test 1, good files: should match day15 exactly. Grand total should be $10,435.08.
print("\n=== test 1: good files ===")
write_files(ranked, "ranked_offers.txt", "offers.csv")
show_text_ranking("ranked_offers.txt", ranked)
grand_total_from_csv("offers.csv", ranked)

#9 test 2, missing files: friendly message, ranking from memory, no crash. Still $10,435.08.
print("\n=== test 2: missing files ===")
show_text_ranking("no_such_ranking.txt", ranked)
grand_total_from_csv("no_such_offers.csv", ranked)

#10 test 3, one bad row: Burlington's total typed as words. It should be skipped and noted;
# the other two still add up: Boston $3,900.00 + Cleveland $3,123.08 = $7,023.08.
print("\n=== test 3: one bad CSV row ===")
bad_csv_name = "offers_bad_row.csv"
with open(bad_csv_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["rank", "city", "hourly_rate", "stipend", "hours", "weekly_total"])
    writer.writerow([1, "Boston", 35, 2500, 40, 3900.0])
    writer.writerow([2, "Burlington", 42, 1900, 36, "three thousand four hundred"])  # the bad value
    writer.writerow([3, "Cleveland", 39.53, 1700, 36, 3123.08])
grand_total_from_csv(bad_csv_name, ranked)

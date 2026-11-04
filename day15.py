import csv  # part of plain Python, nothing to install; imports go at the top of a file

offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]


#1 example Day 15: same ranking as Day 14, copied here so this file runs on its own.
def rank_offers(offer_list, rank_by="weekly_total"):
    if rank_by not in ("weekly_total", "hourly_rate"):
        print(f"unknown rank_by: {rank_by}")
        return []
    # the only place the weekly total is worked out; everything after reads the stored value
    for offer in offer_list:
        offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    return sorted(offer_list, key=lambda offer: offer[rank_by], reverse=True)


ranked = rank_offers(offers)
file_name = "ranked_offers.txt"  # one name, used for both the write and the read, so they can't drift apart

#2 example Day 15: write the ranking to a text file, one offer per line.
# "w" means write: it creates the file, or wipes it and starts fresh if it already exists.
# The "with" block closes (finishes saving) the file the moment the indented lines end.
with open(file_name, "w") as file:
    rank = 1
    for offer in ranked:
        # write() doesn't add a line break on its own like print() does, so "\n" ends each line
        file.write(f"{rank}. {offer['city']}: ${offer['hourly_rate']}/hr, "
                   f"${offer['stipend']:,} stipend, {offer['hours']} hrs, "
                   f"weekly total ${offer['weekly_total']:,.2f}\n")
        rank = rank + 1

print(f"wrote {len(ranked)} offers to {file_name}")

#3 example Day 15: read the file back and print what it contains.
# This starts only after the "with" block above has ended, so the file is fully saved.
# "r" means read: it only looks at the file, never changes it.
with open(file_name, "r") as file:
    contents = file.read()  # the whole file as one piece of text

print(f"\ncontents of {file_name}:")
print(contents)


#4 example Day 15: write the same ranking as a CSV, a header row first, then one row per offer.
# csv (imported at the top) puts the commas in for us, so a stray comma can't break a row.
csv_name = "offers.csv"
# newline="" is what the csv module asks for; without it some systems put a blank line between rows
with open(csv_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["rank", "city", "hourly_rate", "stipend", "hours", "weekly_total"])  # header row
    rank = 1
    for offer in ranked:
        # plain numbers only here (no $ or commas), so a spreadsheet or Python can do math on them later
        writer.writerow([rank, offer["city"], offer["hourly_rate"], offer["stipend"],
                         offer["hours"], round(offer["weekly_total"], 2)])
        rank = rank + 1

print(f"wrote {len(ranked)} offers to {csv_name}")

#5 example Day 15: read the CSV back, print each row, and check the totals.
# Every value read from a CSV comes back as TEXT, even "3900.0" -- same as input() on Day 4.
with open(csv_name, "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)  # take the header row off first so the loop only sees offers
    rows = list(reader)

print(f"\nrows read back from {csv_name}:")
print(f"  header: {header}")
grand_total = 0  # starts at 0 before the loop, like Day 9
for row in rows:
    rank, city, hourly_rate, stipend, hours, weekly_total = row
    print(f"  {row}")
    # convert text -> numbers with float(), then work the total out again from the rate, hours, and stipend
    stored_total = float(weekly_total)
    recomputed_total = float(hourly_rate) * float(hours) + float(stipend)
    # compare rounded to cents, so a tiny float leftover like .0000000001 doesn't count as a mismatch
    if round(recomputed_total, 2) == round(stored_total, 2):
        print(f"     {city}: stored ${stored_total:,.2f} = recomputed ${recomputed_total:,.2f}  OK")
    else:
        print(f"     {city}: stored ${stored_total:,.2f} vs recomputed ${recomputed_total:,.2f}  MISMATCH")
    grand_total = grand_total + stored_total

print(f"grand_total of all weekly totals: ${grand_total:,.2f}")  # should be $10,435.08

# the trap, shown on purpose: "adding" two totals while they're still text just glues them together
first_total_text = rows[0][5]
second_total_text = rows[1][5]
print(f"text + text: {first_total_text + second_total_text}")
print(f"float + float: {float(first_total_text) + float(second_total_text):,.2f}")

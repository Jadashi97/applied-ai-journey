import csv
import sqlite3  # part of plain Python, nothing to install

from offer_ranking import rank_offers  # only used if offers.csv is missing (fallback below)

# Synthetic details that offers.csv doesn't have: each city's state and contract dates.
# Keyed by city so they're attached to the right row, whatever order the CSV is in.
extra_details = {
    "Boston": {"state": "MA", "start": "2027-01-04", "end": "2027-04-04"},
    "Burlington": {"state": "VT", "start": "2027-02-01", "end": "2027-03-28"},
    "Cleveland": {"state": "OH", "start": "2027-01-11", "end": "2027-04-07"},
}

#1 example Day 22: read the three offers from offers.csv (written by day15.py).
# CSV values come back as TEXT (Day 15), so convert each number before storing it.
csv_name = "offers.csv"
offers = []
try:
    with open(csv_name, "r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)  # rank, city, hourly_rate, stipend, hours, weekly_total
        for rank, city, hourly_rate, stipend, hours, weekly_total in reader:
            offers.append({"city": city, "hourly_rate": float(hourly_rate), "stipend": float(stipend),
                           "hours": int(hours), "weekly_total": float(weekly_total)})
    print(f"read {len(offers)} offers from {csv_name}")
except FileNotFoundError:
    # offers.csv is in .gitignore, so a fresh copy of the repo won't have it (Day 16 fallback).
    print(f"couldn't find {csv_name} (run python3 day15.py to make it) -- using the offers in memory")
    offers = rank_offers([
        {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
        {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
        {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
    ])  # rank_offers works out weekly_total with the one shared formula

#2 example Day 22: rebuild offers.db from scratch -- the Day 21 columns plus state.
connection = sqlite3.connect("offers.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS offers")  # so a second run can't double every row (Day 21)
cursor.execute("""
    CREATE TABLE offers (
        city TEXT,
        hourly_rate REAL,
        stipend REAL,
        hours INTEGER,
        weekly_total REAL,
        start TEXT,
        end TEXT,
        state TEXT
    )
""")
for offer in offers:
    details = extra_details[offer["city"]]
    # Naming the columns means the values can't land in the wrong column if the table changes.
    cursor.execute(
        "INSERT INTO offers (city, hourly_rate, stipend, hours, weekly_total, start, end, state) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (offer["city"], offer["hourly_rate"], offer["stipend"], offer["hours"],
         offer["weekly_total"], details["start"], details["end"], details["state"]),
    )
connection.commit()


#3 example Day 22: one function for every query. The SQL has ? marks; the values travel
# separately in params, in the same order. Python never pastes a value into the SQL text.
def print_offers(label, sql, params=()):
    rows = cursor.execute(sql, params).fetchall()
    print(f"\n{label}")
    if not rows:
        print("  no offers found")
        return
    for city, state, hourly_rate, hours, weekly_total in rows:
        print(f"  {city}, {state}: ${hourly_rate:,.2f}/hr, {hours} hrs, weekly total ${weekly_total:,.2f}")


columns = "SELECT city, state, hourly_rate, hours, weekly_total FROM offers"

#4 example Day 22: (1) all offers, best first. Should be Boston, Burlington, Cleveland.
print_offers("(1) all ORDER BY weekly_total DESC:",
             f"{columns} ORDER BY weekly_total DESC")
# (The f-string here only joins two pieces of SQL that WE wrote. No value goes in that way.)

#5 example Day 22: (2) one state. 'MA' is a value, so it goes in as ? -- expect Boston only.
print_offers("(2) WHERE state = ? ('MA'):",
             f"{columns} WHERE state = ?", ("MA",))

#6 example Day 22: (3) AND = both must be true. Over $3,400 AND 36 hours -> Burlington only.
# (Boston is over $3,400 but works 40 hours; Cleveland works 36 but is under $3,400.)
print_offers("(3) WHERE weekly_total > ? AND hours = ? (3400, 36):",
             f"{columns} WHERE weekly_total > ? AND hours = ? ORDER BY weekly_total DESC", (3400, 36))

#7 example Day 22: (4) OR = at least one is true. 36 hours (Burlington, Cleveland)
# OR over $3,800 (Boston) -> all three. OR widens; AND narrows.
print_offers("(4) WHERE hours = ? OR weekly_total > ? (36, 3800):",
             f"{columns} WHERE hours = ? OR weekly_total > ? ORDER BY weekly_total DESC", (36, 3800))

#8 example Day 22: (5) BETWEEN includes BOTH ends (like >= 3100 AND <= 3500).
# ASC = smallest first. Expect Cleveland ($3,123.08) then Burlington ($3,412).
print_offers("(5) WHERE weekly_total BETWEEN ? AND ? ORDER BY weekly_total ASC (3100, 3500):",
             f"{columns} WHERE weekly_total BETWEEN ? AND ? ORDER BY weekly_total ASC", (3100, 3500))

#9 example Day 22: (6) LIMIT keeps only the first N rows after sorting -> the top rate.
# Expect Burlington at $42/hr -- a different winner from the weekly-total ranking (DECISIONS #1).
print_offers("(6) ORDER BY hourly_rate DESC LIMIT ? (1):",
             f"{columns} ORDER BY hourly_rate DESC LIMIT ?", (1,))

#10 example Day 22: (7) a state with no offers -> a clear message, not a crash.
print_offers("(7) WHERE state = ? ('TX'):",
             f"{columns} WHERE state = ?", ("TX",))

#11 example Day 22: grand total. Should be $10,435.08 (Day 15 anchor).
grand_total = cursor.execute("SELECT SUM(weekly_total) FROM offers").fetchone()[0]
print(f"\ngrand_total (SELECT SUM(weekly_total)): ${grand_total:,.2f}")

connection.close()

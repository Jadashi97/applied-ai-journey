import sqlite3  # part of plain Python, nothing to install: a whole database in one file

from offer_ranking import rank_offers  # Day 17 module: the ONE place the weekly total is worked out

# Same three synthetic offers as Day 15/17.
offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40,
     "start": "2027-01-04", "end": "2027-04-04"},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36,
     "start": "2027-02-01", "end": "2027-03-28"},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36,
     "start": "2027-01-11", "end": "2027-04-07"},
]

#1 example Day 21: work out each weekly total once, with the same function as Day 17,
# so the database can't drift from the anchor by using a second copy of the formula.
rank_offers(offers)  # adds offer["weekly_total"] to each offer; we only need that, not the order here

#2 example Day 21: open (or create) the database file and make a fresh offers table.
db_name = "offers.db"
connection = sqlite3.connect(db_name)  # creates offers.db the first time; opens it after that
cursor = connection.cursor()           # the cursor is what sends SQL to the database and holds results

# DROP first so running this file twice doesn't insert the offers twice.
# Without it, the second run would have 6 rows and a grand total of $20,870.16 (double-counting, Day 2).
cursor.execute("DROP TABLE IF EXISTS offers")
cursor.execute("""
    CREATE TABLE offers (
        city TEXT,
        hourly_rate REAL,
        stipend REAL,
        hours INTEGER,
        weekly_total REAL,
        start TEXT,
        end TEXT
    )
""")  # TEXT = words, REAL = decimal number, INTEGER = whole number

#3 example Day 21: insert the three offers, one row each.
for offer in offers:
    # The ? marks are placeholders: sqlite3 slots the values in safely, in this order.
    # Never build SQL with an f-string -- a city like "O'Hare" would break the quotes.
    cursor.execute(
        "INSERT INTO offers VALUES (?, ?, ?, ?, ?, ?, ?)",
        (offer["city"], offer["hourly_rate"], offer["stipend"], offer["hours"],
         offer["weekly_total"], offer["start"], offer["end"]),
    )
connection.commit()  # saves the inserts to offers.db; without it they'd be lost when the file closes
print(f"saved {len(offers)} offers to {db_name}")


#4 example Day 21: one function to run a query and print the rows, or a clear message if none match.
def print_offers(label, sql):
    rows = cursor.execute(sql).fetchall()  # fetchall() gives a list of rows; each row is a tuple
    print(f"\n{label}")
    if not rows:  # an empty list counts as false (Day 14) -- no rows is normal, not a crash
        print("  no offers found")
        return
    for city, weekly_total, hours in rows:  # each row has exactly the 3 columns we SELECTed
        print(f"  {city}: weekly total ${weekly_total:,.2f}, {hours} hrs")


#5 example Day 21: all offers, best first. ORDER BY ... DESC is SQL's sorted(..., reverse=True).
print_offers("all offers ORDER BY weekly_total DESC:",
             "SELECT city, weekly_total, hours FROM offers ORDER BY weekly_total DESC")

#6 example Day 21: WHERE keeps only rows that pass the test, like an if inside a loop.
# Expect Boston ($3,900) and Burlington ($3,412); Cleveland ($3,123.08) is under $3,400.
print_offers("WHERE weekly_total > 3400:",
             "SELECT city, weekly_total, hours FROM offers WHERE weekly_total > 3400 "
             "ORDER BY weekly_total DESC")

#7 example Day 21: SQL uses ONE = to compare (Python uses ==). Expect Burlington and Cleveland.
print_offers("WHERE hours = 36:",
             "SELECT city, weekly_total, hours FROM offers WHERE hours = 36 "
             "ORDER BY weekly_total DESC")

#8 example Day 21: SUM adds up a whole column -- the database does the Day 9 running-total loop.
# fetchone() gives one row; [0] takes its only value. Should be $10,435.08.
grand_total = cursor.execute("SELECT SUM(weekly_total) FROM offers").fetchone()[0]
print(f"\ngrand_total (SELECT SUM(weekly_total)): ${grand_total:,.2f}")

#9 example Day 21: a query that matches nothing. No offer is over $10,000 a week.
print_offers("WHERE weekly_total > 10000:",
             "SELECT city, weekly_total, hours FROM offers WHERE weekly_total > 10000")

# Gotcha: SUM over zero rows gives None, not 0. Formatting None with :,.2f would crash,
# so check for None first.
empty_total = cursor.execute("SELECT SUM(weekly_total) FROM offers WHERE weekly_total > 10000").fetchone()[0]
if empty_total is None:  # same "is None" check as Day 13
    print("  SUM of no offers: none to add up")
else:
    print(f"  SUM of matching offers: ${empty_total:,.2f}")

connection.close()  # done with the database file

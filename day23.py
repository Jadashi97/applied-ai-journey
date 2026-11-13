import sqlite3  # part of plain Python, nothing to install

from offer_ranking import rank_offers  # works out weekly_total with the one shared formula

#1 example Day 23: the same 3 synthetic offers as Day 22, with state and dates.
offers = rank_offers([
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
])
extra_details = {
    "Boston": {"state": "MA", "start": "2027-01-04", "end": "2027-04-04"},
    "Burlington": {"state": "VT", "start": "2027-02-01", "end": "2027-03-28"},
    "Cleveland": {"state": "OH", "start": "2027-01-11", "end": "2027-04-07"},
}

#2 example Day 23: rebuild the offers table exactly like Day 22.
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
    cursor.execute(
        "INSERT INTO offers (city, hourly_rate, stipend, hours, weekly_total, start, end, state) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (offer["city"], offer["hourly_rate"], offer["stipend"], offer["hours"],
         offer["weekly_total"], details["start"], details["end"], details["state"]),
    )

#3 example Day 23: a SECOND table, one row per state. The two tables share the state column --
# that shared column is what a JOIN matches on. NH has no offer on purpose (see query 3).
# Figures are the public Vivian numbers given in the task, typed in as-is (not re-checked here).
state_pay = [
    ("MA", 3021, 4055, "Yes"),
    ("VT", 3241, 4070, "Yes"),
    ("OH", 2550, 3520, "Yes"),
    ("NH", 2901, 3696, "Yes"),
]
cursor.execute("DROP TABLE IF EXISTS state_pay")  # same reason as above
cursor.execute("""
    CREATE TABLE state_pay (
        state TEXT,
        avg_pay REAL,
        max_pay REAL,
        license_required TEXT
    )
""")
for state, avg_pay, max_pay, license_required in state_pay:
    cursor.execute(
        "INSERT INTO state_pay (state, avg_pay, max_pay, license_required) VALUES (?, ?, ?, ?)",
        (state, avg_pay, max_pay, license_required),
    )
connection.commit()

#4 example Day 23: (1) INNER JOIN = only rows that match in BOTH tables.
# 3 offers x their state's pay row -> 3 rows. NH has no offer, so it's left out.
print("\n(1) INNER JOIN offers + state_pay ON state:")
rows = cursor.execute("""
    SELECT offers.city, offers.state, offers.weekly_total, state_pay.avg_pay, state_pay.max_pay
    FROM offers
    INNER JOIN state_pay ON offers.state = state_pay.state
    ORDER BY offers.weekly_total DESC
""").fetchall()
for city, state, weekly_total, avg_pay, max_pay in rows:
    print(f"  {city}, {state}: offer ${weekly_total:,.2f} | state avg ${avg_pay:,.2f}, max ${max_pay:,.2f}")

#5 example Day 23: (2) math across the two tables. "AS difference" names the new column
# so ORDER BY can use it. Biggest gap above the state average first.
print("\n(2) weekly_total - avg_pay, ORDER BY difference DESC:")
rows = cursor.execute("""
    SELECT offers.city, offers.weekly_total, state_pay.avg_pay,
           offers.weekly_total - state_pay.avg_pay AS difference
    FROM offers
    INNER JOIN state_pay ON offers.state = state_pay.state
    ORDER BY difference DESC
""").fetchall()
for city, weekly_total, avg_pay, difference in rows:
    print(f"  {city}: ${weekly_total:,.2f} - ${avg_pay:,.2f} = ${difference:,.2f} above avg")

#6 example Day 23: (3) LEFT JOIN = keep EVERY row from the left table (state_pay),
# even with no match on the right. NH has no offer -> its offer columns come back as None.
print("\n(3) state_pay LEFT JOIN offers ON state:")
rows = cursor.execute("""
    SELECT state_pay.state, state_pay.avg_pay, offers.city, offers.weekly_total
    FROM state_pay
    LEFT JOIN offers ON state_pay.state = offers.state
    ORDER BY state_pay.state
""").fetchall()
for state, avg_pay, city, weekly_total in rows:
    if city is None:  # no matching offer -> None, not 0 (same idea as SUM of no rows, Day 21)
        print(f"  {state}: state avg ${avg_pay:,.2f} | no offer")
    else:
        print(f"  {state}: state avg ${avg_pay:,.2f} | {city} ${weekly_total:,.2f}")

#7 example Day 23: (4) GROUP BY = one output row per distinct value, with the math done
# inside each group. Two offers are 36 hrs, one is 40 -> 2 rows. COUNT shows the group size.
print("\n(4) GROUP BY hours, SUM and AVG of weekly_total:")
rows = cursor.execute("""
    SELECT hours, COUNT(*), SUM(weekly_total), AVG(weekly_total)
    FROM offers
    GROUP BY hours
    ORDER BY hours
""").fetchall()
for hours, count, total, average in rows:
    print(f"  {hours} hrs: {count} offer(s), sum ${total:,.2f}, avg ${average:,.2f}")

#8 example Day 23: (5) GROUP BY state. One offer per state here, so each sum = that offer.
print("\n(5) GROUP BY state, SUM of weekly_total:")
rows = cursor.execute("""
    SELECT state, SUM(weekly_total)
    FROM offers
    GROUP BY state
    ORDER BY SUM(weekly_total) DESC
""").fetchall()
for state, total in rows:
    print(f"  {state}: ${total:,.2f}")

#9 example Day 23: (6) HAVING filters GROUPS after the math; WHERE filters ROWS before it.
# 36-hr avg is $3,267.54 (under 3400) even though Burlington alone is $3,412 -> only 40 hrs.
print("\n(6) GROUP BY hours HAVING AVG(weekly_total) > ? (3400):")
rows = cursor.execute("""
    SELECT hours, AVG(weekly_total)
    FROM offers
    GROUP BY hours
    HAVING AVG(weekly_total) > ?
""", (3400,)).fetchall()
if not rows:
    print("  no groups found")
for hours, average in rows:
    print(f"  {hours} hrs: avg ${average:,.2f}")

#10 example Day 23: (7) a state with no offers -> a clear message, not a crash.
print("\n(7) WHERE state = ? ('TX'):")
rows = cursor.execute("""
    SELECT city, state, weekly_total
    FROM offers
    WHERE state = ?
""", ("TX",)).fetchall()
if not rows:
    print("  no offers found")
for city, state, weekly_total in rows:
    print(f"  {city}, {state}: ${weekly_total:,.2f}")

#11 example Day 23: grand total. Should be $10,435.08 (Day 15 anchor).
grand_total = cursor.execute("SELECT SUM(weekly_total) FROM offers").fetchone()[0]
print(f"\ngrand_total (SELECT SUM(weekly_total)): ${grand_total:,.2f}")

connection.close()

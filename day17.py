from datetime import date  # plain Python's date type: knows real calendars, leap years, month lengths

from offer_ranking import rank_offers  # our OWN module: Python finds offer_ranking.py in this same folder

#1 example Day 17: the same three offers as Day 15, now with start and end dates.
# Dates are written as text "YYYY-MM-DD", the way a CSV or a contract PDF would give them.
offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40,
     "start": "2027-01-04", "end": "2027-04-04"},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36,
     "start": "2027-01-11", "end": "2027-04-07"},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36,
     "start": "2027-02-01", "end": "2027-03-28"},
]


#2 example Day 17: turn the date text into real dates and work out the contract length.
def contract_length(offer):
    # like float() on Day 4: text in, a real value out. Bad text -> ValueError (Day 16).
    start_date = date.fromisoformat(offer["start"])
    end_date = date.fromisoformat(offer["end"])
    # end minus start gives the days BETWEEN them. A contract works both the first and the
    # last day, so +1 counts both (Jan 4 to Jan 4 is 1 day worked, not 0). Classic off-by-one.
    days = (end_date - start_date).days + 1
    return days


#3 example Day 17: rank with the imported function -- same call as day15, same result expected.
ranked = rank_offers(offers)

print("ranked by weekly total, with contract length:")
grand_total = 0  # starts at 0 before the loop, like Day 9
rank = 1
for offer in ranked:
    days = contract_length(offer)
    weeks = days // 7       # // divides and drops the remainder: 87 // 7 = 12
    extra_days = days % 7   # % gives the remainder (Day 10): 87 % 7 = 3
    print(f"  {rank}. {offer['city']}: weekly total ${offer['weekly_total']:,.2f} | "
          f"{offer['start']} to {offer['end']} = {days} days ({weeks} weeks {extra_days} days)")
    grand_total = grand_total + offer["weekly_total"]
    rank = rank + 1

print(f"grand_total of all weekly totals: ${grand_total:,.2f}")  # should be $10,435.08 like day15

#4 example Day 17: a date that doesn't exist on the calendar. date() checks it; caught like Day 16.
bad_offer = {"city": "Denver", "start": "2027-02-30", "end": "2027-05-01"}  # February has no 30th
try:
    days = contract_length(bad_offer)
    print(f"{bad_offer['city']}: {days} days")
except ValueError as error:
    print(f"\nskipped {bad_offer['city']}: bad date ({error})")

#1 example Make a list of cities and print each one on its own line.
cities = ["Boston", "Cleveland", "Burlington"]
for city in cities:
    print(city)

#2 example Make a list of hourly rates and print each one.
hourly_rates = [35, 39.53, 42]
for rate in hourly_rates:
    print(f"hourly_rate: ${rate}")

#3 example Loop over the cities and print one sentence per city.
for city in cities:
    print(f"I have a contract offer in {city}.")

#4 example Make a list of 3 offer dictionaries: Boston and Cleveland from Day 8, plus one more fake offer.
offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 36},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1673, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]
print(offers)

#5 example Loop over the offers and print just the city of each.
for offer in offers:
    print(offer["city"])

#6 example Loop over the offers and print city and hourly rate together.
for offer in offers:
    print(f"{offer['city']}: ${offer['hourly_rate']}")

#7 example Loop over the offers, work out each weekly total once per offer, and print it.
for offer in offers:
    weekly_total = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    print(f"{offer['city']} weekly_total: ${weekly_total:,.2f}")

#8 example Keep a running total of all weekly totals, and print it only at the end.
all_offers_total = 0  # start at 0 before the loop, or it resets every time
for offer in offers:
    weekly_total = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    all_offers_total = all_offers_total + weekly_total
print(f"all_offers_total: ${all_offers_total:,.2f}")  # not indented, so it prints once

#9 example Loop over a range of numbers and print each one. range(1, 6) stops before 6.
for number in range(1, 6):
    print(number)

#10 example Loop over one offer dictionary and print each label and value, one per line.
for label, value in offers[1].items():
    print(f"{label}: {value}")

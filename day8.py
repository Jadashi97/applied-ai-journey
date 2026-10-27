#1 example Make one Boston offer with labels for city, hourly rate, stipend, and hours.
boston_offer = {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 36}
print(boston_offer)

#2 example Print just the rate, by its label.
print(boston_offer["hourly_rate"])

#3 example Print just the stipend.
print(boston_offer["stipend"])

#4 example Change the hours, then print the offer again to prove it updated.
boston_offer["hours"] = 40
print(boston_offer)

#5 example Add a new label for contract weeks.
boston_offer["contract_weeks"] = 13
print(boston_offer)

#6 example Print all the labels, then print all the values.
print(boston_offer.keys())
print(boston_offer.values())

#7 example Make a second, Cleveland offer and print both rates side by side.
cleveland_offer = {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1673, "hours": 36}
print(f"Boston: ${boston_offer['hourly_rate']} | Cleveland: ${cleveland_offer['hourly_rate']}")

#8 example Work out the weekly total once and store it under a new label.
boston_offer["weekly_total"] = boston_offer["hourly_rate"] * boston_offer["hours"] + boston_offer["stipend"]
print(f"weekly_total: ${boston_offer['weekly_total']:,.2f}")

#9 example Check whether a label exists, like housing, before you try to use it.
print("housing" in boston_offer)

#10 example Ask for a missing label with a safe fallback, so it doesn't crash.
print(boston_offer.get("housing", "not included"))

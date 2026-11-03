offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]

#1 example Day 11: loop through the offers and keep only the best one so far.
best_offer = None  # None means "nothing yet"
best_total = 0
for offer in offers:
    weekly_total = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    if weekly_total > best_total:  # only update when this total beats the best so far
        best_total = weekly_total
        best_offer = offer
print(f"Day 11 best: {best_offer['city']} ${best_total:,.2f}")


#2 example Day 12: wrap that loop in a function that takes a list of offers and returns the best one.
def find_best_offer_day12(offer_list):
    best_offer = None
    best_total = 0
    for offer in offer_list:
        weekly_total = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
        if weekly_total > best_total:
            best_total = weekly_total
            best_offer = offer
    return best_offer  # hand the winner back instead of printing it

#3 example Day 12: test it on two different lists. Only Cleveland's stipend changes in the second one.
winner = find_best_offer_day12(offers)
print(f"Day 12 list 1 winner: {winner['city']}")

offers_with_bigger_stipend = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 3000, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]
winner = find_best_offer_day12(offers_with_bigger_stipend)
print(f"Day 12 list 2 winner: {winner['city']}")  # the winner changes, so nothing is hard-coded


#4 example Day 13: add a ranking choice. rank_by="weekly_total" is the default when no choice is given.
def find_best_offer(offer_list, rank_by="weekly_total"):
    best_offer = None
    best_score = 0
    for offer in offer_list:
        # store the weekly total on the offer once, so callers can print it without redoing the math
        offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
        if rank_by == "weekly_total":
            score = offer["weekly_total"]
        elif rank_by == "hourly_rate":
            score = offer["hourly_rate"]
        else:
            print(f"unknown rank_by: {rank_by}")
            return None
        if score > best_score:
            best_score = score
            best_offer = offer
    return best_offer  # an empty list never enters the loop, so this returns None

#5 example Day 13: no choice given, so it ranks by weekly total. Boston should win at $3,900.
winner = find_best_offer(offers)
print(f"Day 13 by total: {winner['city']} ${winner['weekly_total']:,.2f}")

#6 example Day 13: rank the same list by hourly rate. Burlington should win at $42.
winner = find_best_offer(offers, rank_by="hourly_rate")
print(f"Day 13 by rate: {winner['city']} ${winner['hourly_rate']}")

#7 example Day 13: an empty list returns None instead of crashing.
winner = find_best_offer([])
if winner is None:  # check before using it; winner['city'] on None would crash
    print("Day 13 empty list: no offers to compare")
else:
    print(f"Day 13 empty list: {winner['city']}")

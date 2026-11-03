offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]


#1 example Day 14: rank every offer, not just the winner. Built from Day 13's find_best_offer.
def rank_offers(offer_list, rank_by="weekly_total"):
    if rank_by not in ("weekly_total", "hourly_rate"):
        print(f"unknown rank_by: {rank_by}")
        return []
    # the only place the weekly total is worked out; everything after reads the stored value
    for offer in offer_list:
        offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    # sorted() hands back a new list in order; key says what to sort on, reverse=True puts the biggest first
    return sorted(offer_list, key=lambda offer: offer[rank_by], reverse=True)  # empty list in, empty list out


#2 example Day 14: one print function, so the ranked-list layout isn't copied three times.
def print_ranking(label, ranked):
    print(f"\n{label}")
    if not ranked:  # an empty list counts as false, so this catches "no offers"
        print("  no offers to compare")
        return
    rank = 1
    for offer in ranked:
        print(f"  {rank}. {offer['city']}: ${offer['hourly_rate']}/hr, "
              f"${offer['stipend']:,} stipend, {offer['hours']} hrs, "
              f"weekly total ${offer['weekly_total']:,.2f}")
        rank = rank + 1


#3 example Day 14: rank by weekly total (the default). Boston should be 1st at $3,900.
print_ranking("Day 14 list 1 by weekly total:", rank_offers(offers))

#4 example Day 14: same list by hourly rate. Burlington should be 1st at $42.
print_ranking("Day 14 list 1 by hourly rate:", rank_offers(offers, rank_by="hourly_rate"))

#5 example Day 14: second list, only Cleveland's stipend changes ($1,700 -> $3,000). Cleveland should jump to 1st.
offers_with_bigger_stipend = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 3000, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]
print_ranking("Day 14 list 2 by weekly total:", rank_offers(offers_with_bigger_stipend))

#6 example Day 14: an empty list gives an empty ranking instead of crashing.
print_ranking("Day 14 empty list:", rank_offers([]))

# offer_ranking.py -- the offer-ranking logic from Days 14-16, kept in one place.
# A "module" is just a .py file that other files can import. This one only DEFINES
# functions; it never prints or runs anything on its own, so importing it is silent.


def rank_offers(offer_list, rank_by="weekly_total"):
    if rank_by not in ("weekly_total", "hourly_rate"):
        print(f"unknown rank_by: {rank_by}")
        return []
    # the only place the weekly total is worked out; everything after reads the stored value
    for offer in offer_list:
        offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    return sorted(offer_list, key=lambda offer: offer[rank_by], reverse=True)

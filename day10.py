offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 36},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1673, "hours": 36},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
]

#1 example Count up with a while-loop: start at 1, print it, add 1 each time, stop at 5.
count = 1
while count <= 5:
    print(count)
    count = count + 1  # without this line the loop never ends

#2 example Count down with a while-loop: start at 5, print it, subtract 1 each time, stop at 1.
count = 5
while count >= 1:
    print(count)
    count = count - 1

#3 example While-loop through numbers 1 to 6, printing "even" or "odd" for each one.
number = 1
while number <= 6:
    if number % 2 == 0:  # % gives the remainder; even numbers have 0 left over after dividing by 2
        print(f"{number} even")
    else:
        print(f"{number} odd")
    number = number + 1

#4 example Keep adding Boston's $3,760 weekly total, but never let the total go over $10,000.
boston_weekly_total = 3760
total = 0
while total < 10000:
    if total + boston_weekly_total <= 10000:  # check first: would this addition stay under the limit?
        total = total + boston_weekly_total
        print(f"total: ${total:,.2f}")
    else:
        print(f"stopping: next addition would make ${total + boston_weekly_total:,.2f}")
        break  # break ends the loop right away
print(f"final total: ${total:,.2f}")

#5 example If/else on one offer: $40 or more is "high rate", otherwise "standard rate".
burlington = offers[2]
if burlington["hourly_rate"] >= 40:
    print("high rate")
else:
    print("standard rate")

#6 example If/elif/else on a weekly total: $3,500+ is "top tier", $3,100+ is "good", otherwise "lower".
weekly_total = burlington["hourly_rate"] * burlington["hours"] + burlington["stipend"]
if weekly_total >= 3500:
    print(f"${weekly_total:,.2f} top tier")
elif weekly_total >= 3100:
    print(f"${weekly_total:,.2f} good")
else:
    print(f"${weekly_total:,.2f} lower")

#7 example While-loop over the offers by position, printing each city, stopping when we run out.
position = 0
while position < len(offers):
    print(offers[position]["city"])
    position = position + 1

#8 example While-loop on hours: start at 36, print it, add 1 each time, stop at 40.
hours = 36
while hours <= 40:
    print(f"hours: {hours}")
    hours = hours + 1

#9 example If with two conditions: Boston AND a stipend of $2,000 or more.
boston = offers[0]
if boston["city"] == "Boston" and boston["stipend"] >= 2000:
    print("matches")
else:
    print("doesn't match")

#10 example Combine them: label each offer "top offer" if its weekly total is $3,500 or more.
position = 0
while position < len(offers):
    offer = offers[position]
    weekly_total = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
    if weekly_total >= 3500:
        print(f"{offer['city']}: ${weekly_total:,.2f} top offer")
    else:
        print(f"{offer['city']}: ${weekly_total:,.2f} standard offer")
    position = position + 1

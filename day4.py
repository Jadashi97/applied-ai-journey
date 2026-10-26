#1 example Ask for the bill amount and turn the text into a number with float().
bill = float(input("Bill amount: $"))

#2 example Ask for the tip percent, like 20 for 20%.
tip_percent = float(input("Tip percent: "))

#3 example Ask how many people are splitting the bill. Use int() since people are whole numbers.
people = int(input("Number of people: "))

#4 example Do the math: tip, total, and each person's share.
tip = bill * tip_percent / 100
total = bill + tip
per_person = total / people

#5 example Print the results with commas and 2 decimals.
print(f"tip: ${tip:,.2f}")
print(f"total: ${total:,.2f}")
print(f"per_person: ${per_person:,.2f}")

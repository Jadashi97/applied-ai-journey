#1 example Ask for hours worked this week. Use float() in case of partial hours like 36.5.
hours = float(input("Hours worked: "))

#2 example Ask for the taxable hourly rate.
hourly_rate = float(input("Hourly rate: $"))

#3 example Ask for the weekly stipend (the non-taxed part of the split).
stipend = float(input("Weekly stipend: $"))

#4 example Do the math: taxable pay from hours, then add the stipend for the weekly total.
taxable_pay = hours * hourly_rate
weekly_total = taxable_pay + stipend

#5 example Print the results with commas and 2 decimals.
print(f"taxable_pay: ${taxable_pay:,.2f}")
print(f"stipend: ${stipend:,.2f}")
print(f"weekly_total: ${weekly_total:,.2f}")

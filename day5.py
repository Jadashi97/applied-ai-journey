#Make a list of your four filing states: Ohio, Vermont, Rhode Island, Massachusetts. Print the whole list.
filing_states = ["Ohio", "Vermont", "Rhode Island", "Massachusetts"]
print(filing_states)

#Print just the first state in the list (index 0).
print(filing_states[0])

#Print just the first state in the list (index 0).
print(filing_states[0])

#Print just the last state using a negative index.
print(filing_states[-1])

#Add "Connecticut" to the end of the list with append(), then print the list.
filing_states.append("Connecticut")
print(filing_states)

#Make a list of three weekly pay numbers: 3716, 3673, 3603. Print the biggest one using max().
weekly_pays = [3716, 3673, 3603]
print(max(weekly_pays))

#Change the second pay number to 4000 (index assignment), then print the list.
weekly_pays[1] = 4000
print(weekly_pays)

#Loop through the states list with a for loop and print each state on its own line.
for state in filing_states:
    print(state)

#Loop through the pay list and print each one as Weekly pay: $3716 using an f-string.
for pay in weekly_pays:
    print(f"Weekly pay: ${pay}")

#Make a list of your two agencies: "Aya", "Triage". Use len() to print how many are in the list.
agencies = ["Aya", "Triage"]
print(len(agencies))

#Make a list of lake numbers [40, 41] and loop through it, printing Lake 40 done style lines with an f-string.
lake_numbers = [40, 41]
for lake in lake_numbers:
    print(f"Lake {lake} done")

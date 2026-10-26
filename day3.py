#1 example Start with a city/state string like "Cleveland, Ohio" and slice out just the state name.
city_state = "Cleveland, Ohio"
state = city_state.split(", ")[1]
print(state)

#2 example Take a zip code string like "44114" and slice out just the last two digits.
zip_code = "44114"
last_two_digits = zip_code[-2:]
print(last_two_digits)

#3 Take a facility name like "MetroHealth Medical Center" and print only the first 5 characters.
facility_name = "MetroHealth Medical Center"
first_five_characters = facility_name[:5]
print(first_five_characters)

#4 example Clean up a messy name with extra spaces like "   MetroHealth   " using strip().
messy_name = "   MetroHealth   "
print(messy_name.strip())

#5 example Turn a shouted state like "OHIO" into title case with title().
shouted_state = "OHIO"
print(shouted_state.title())

#6 example Make an agency name all lowercase with lower() so "AYA Healthcare" matches "aya healthcare".
agency = "AYA Healthcare"
print(agency.lower() == "aya healthcare")

#7 example Fix a typo in a facility name with replace().
typo_name = "MetroHelth Medical Center"
print(typo_name.replace("Helth", "Health"))

#8 example Clean a phone number like "(216) 778-7800" down to just digits by removing symbols and spaces.
phone = "(216) 778-7800"
print(phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", ""))

#9 example Format pay with commas and 2 decimals using an f-string, like $3,716.00.
weekly_pay = 4033
print(f"Weekly pay: ${weekly_pay:,.2f}")

#10 example Join a city and state into one string, then check its length with len().
city = "Cleveland"
state_name = "Ohio"
print(f"{city}, {state_name} has {len(city + ', ' + state_name)} characters")

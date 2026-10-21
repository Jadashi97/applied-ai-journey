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
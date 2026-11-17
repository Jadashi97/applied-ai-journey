import json

import requests  # outside library for web requests: pip install requests

# JSONPlaceholder is a free practice API. Its users are made-up sample data, not real people.
# This endpoint needs no key, so nothing secret is used here (see .env.example for where a key would go).
url = "https://jsonplaceholder.typicode.com/users/1"
summary_name = "api_summary.json"
timeout_seconds = 10  # one number used by both the request and the message, so they can't disagree

#1 example Day 25: ask the API for one user. timeout means "give up after timeout_seconds (10)"
# instead of waiting forever if the server never answers.
try:
    response = requests.get(url, timeout=timeout_seconds)
except requests.exceptions.Timeout:
    print(f"no answer from {url} within {timeout_seconds} seconds -- try again later")
    response = None
except requests.exceptions.ConnectionError:
    # no internet, a wrong address, or the network blocking the site
    print(f"couldn't connect to {url} -- check the internet connection and the address")
    response = None

#2 example Day 25: only use the answer if the status code is 200 ("OK").
# 404 means "not found", 500 means "the server broke" -- either way there's no user to read.
if response is not None and response.status_code != 200:
    print(f"the API answered with status {response.status_code}, not 200 -- nothing saved")
    response = None

if response is not None:
    #3 example Day 25: turn the JSON text into Python dicts and lists (like Day 8's dictionaries).
    # The city sits one level down: the user has an "address" dict, and the city is inside it.
    try:
        user = response.json()
        name = user["name"]
        city = user["address"]["city"]
    except (ValueError, KeyError) as error:  # not JSON at all, or a field we expected is missing
        print(f"the answer wasn't the user data we expected ({error}) -- nothing saved")
    else:  # runs only if the try block had no error
        print(f"status: {response.status_code}")
        print(f"name: {name}")
        print(f"city: {city}")

        #4 example Day 25: save just the three values. Saved only on success, so a failed
        # run can't overwrite a good api_summary.json with an empty or wrong one.
        summary = {"name": name, "city": city, "status_code": response.status_code}
        with open(summary_name, "w") as file:
            json.dump(summary, file, indent=2)  # indent=2 makes it easy to read
            file.write("\n")
        print(f"saved {summary_name}")

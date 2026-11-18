import json

# Day 26: first LLM call. Python does the math; the model is only asked to rank and explain,
# and its answer is checked against Python's numbers before anything is saved.
#
# Before using a real key, know the limits (CLAUDE.md "AI work"):
#   cost     -- every real call is billed per token (this prompt is small: likely well under 1 cent).
#   privacy  -- whatever is in the prompt is sent to the provider. Only synthetic offers go here,
#               never real names, pay stubs or contracts.
#   accuracy -- a model can get a sum or an order wrong while sounding sure. That's why every
#               total is re-checked below, and a human still reads "reason" before trusting it.

offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
]
env_name = ".env"                  # holds the real key; git-ignored, never committed
output_name = "llm_ranking.json"
model_name = "claude-opus-5-5"
timeout_seconds = 30

#1 example Day 26: Python works out the totals -- the source of truth the model is checked against.
for offer in offers:
    offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
expected = sorted(offers, key=lambda offer: offer["weekly_total"], reverse=True)  # Day 14 ranking
expected_totals = {offer["city"]: round(offer["weekly_total"], 2) for offer in offers}
expected_order = [offer["city"] for offer in expected]

print("recomputed weekly totals:")
for offer in expected:
    print(f"  {offer['city']}: ${offer['weekly_total']:,.2f}")
grand_total = sum(offer["weekly_total"] for offer in offers)
print(f"grand_total: ${grand_total:,.2f}")
anchor = {"Boston": 3900.00, "Burlington": 3412.00, "Cleveland": 3123.08}
anchor_ok = expected_totals == anchor and round(grand_total, 2) == 10435.08
print(f"matches Day 15 anchor: {anchor_ok}")

#2 example Day 26: the prompts. The system prompt sets the rules; the user prompt holds the data.
system_prompt = (
    "You rank travel-nurse contract offers. Reply with JSON only: no prose, no markdown, "
    "no code fences. Use exactly these keys: "
    '"ranking" (a list of objects, each with exactly "city" and "weekly_total"), '
    '"best_city" (the city with the highest weekly_total), and '
    '"reason" (one or two plain sentences). '
    "weekly_total is hourly_rate * hours + stipend, as a number rounded to 2 decimals. "
    "Order ranking from highest weekly_total to lowest."
)
offer_lines = "\n".join(
    f"- {offer['city']}: hourly_rate {offer['hourly_rate']}, hours {offer['hours']}, "
    f"stipend {offer['stipend']}"
    for offer in offers
)
user_prompt = f"Rank these offers by weekly_total:\n{offer_lines}"


#3 example Day 26: read LLM_API_KEY from .env. A tiny reader instead of a new library:
# each line looks like NAME=value; blank lines and # comments are skipped.
def read_env_key(name):
    try:
        with open(env_name, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() == name:
                    value = value.strip()
                    # the placeholder from .env.example is not a real key
                    if value and value != "your_key_here":
                        return value
    except FileNotFoundError:
        pass  # no .env at all -> no key
    return None


#4 example Day 26: the stub -- a fixed answer typed in by hand from the Day 15 anchor,
# NOT built from the recomputed totals. If it were built from them, the check in #6 would
# always pass and prove nothing. It lets everything after it run without a key or any cost.
def stub_reply():
    return json.dumps({
        "ranking": [
            {"city": "Boston", "weekly_total": 3900.00},
            {"city": "Burlington", "weekly_total": 3412.00},
            {"city": "Cleveland", "weekly_total": 3123.08},
        ],
        "best_city": "Boston",
        "reason": "Boston has the highest weekly total because its 40 hours and $2,500 stipend "
                  "outweigh its lower hourly rate.",
    })


#5 example Day 26: call_llm() gives back the model's reply as text, plus where it came from.
# Returns (None, source) if the real call fails, so the caller saves nothing.
def call_llm(system_text, user_text):
    api_key = read_env_key("LLM_API_KEY")
    if api_key is None:
        print("log: no key found, using stub")
        return stub_reply(), "stub"

    # Imported only here, so the stub path above runs even without the anthropic library.
    import anthropic

    # The key is passed in from .env, never typed into this file. max_retries=0 so the
    # 30-second timeout really means 30 seconds (the library otherwise retries twice).
    client = anthropic.Anthropic(api_key=api_key, timeout=timeout_seconds, max_retries=0)
    try:
        response = client.beta.messages.create(
            model=model_name,
            max_tokens=16000,
            system=system_text,
            messages=[{"role": "user", "content": user_text}],
            output_config={"effort": "low"},  # a short ranking task doesn't need deep thinking
            # if the model declines, the API retries on a suitable fallback model in the same call
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except anthropic.APITimeoutError:  # checked first: it's a kind of connection error
        print(f"log: no answer within {timeout_seconds} seconds -- nothing saved")
        return None, model_name
    except anthropic.APIConnectionError:
        print("log: couldn't reach the API (internet or network blocked) -- nothing saved")
        return None, model_name
    except anthropic.AuthenticationError:
        print("log: the key in .env was rejected -- check it, nothing saved")
        return None, model_name
    except anthropic.RateLimitError:
        print("log: rate limited -- wait and try again, nothing saved")
        return None, model_name
    except anthropic.APIStatusError as error:
        print(f"log: the API answered with status {error.status_code} -- nothing saved")
        return None, model_name

    if response.stop_reason == "refusal":
        print("log: the model declined this request -- nothing saved")
        return None, response.model
    # The reply can hold several blocks (e.g. thinking); only the text blocks are the answer.
    text = "".join(block.text for block in response.content if block.type == "text")
    print(f"log: tokens used -- input {response.usage.input_tokens}, output {response.usage.output_tokens}")
    return text, response.model


#6 example Day 26: check the reply. Every problem is collected, so one run shows all of them.
# An empty list means the reply passed every check.
def validate(reply_text):
    try:
        reply = json.loads(reply_text)
    except (TypeError, json.JSONDecodeError) as error:
        return None, [f"not valid JSON ({error})"]

    problems = []
    if not isinstance(reply, dict) or set(reply) != {"ranking", "best_city", "reason"}:
        keys = sorted(reply) if isinstance(reply, dict) else type(reply).__name__
        return None, [f"keys must be exactly ranking, best_city, reason (got {keys})"]

    ranking = reply["ranking"]
    if not isinstance(ranking, list) or len(ranking) != len(offers):
        return None, [f"ranking must be a list of {len(offers)} offers"]
    for item in ranking:
        if not isinstance(item, dict) or set(item) != {"city", "weekly_total"}:
            return None, [f"each ranking item needs exactly city and weekly_total (got {item})"]
        total = item["weekly_total"]
        # bool is excluded on purpose: in Python, True counts as the number 1
        if not isinstance(total, (int, float)) or isinstance(total, bool):
            problems.append(f"{item['city']}: weekly_total is not a number ({total!r})")
        elif item["city"] not in expected_totals:
            problems.append(f"unknown city {item['city']!r}")
        elif round(total, 2) != expected_totals[item["city"]]:
            problems.append(f"{item['city']}: model says ${total:,.2f}, "
                            f"Python says ${expected_totals[item['city']]:,.2f}")

    cities = [item["city"] for item in ranking]
    if sorted(cities) != sorted(expected_totals):
        problems.append(f"cities must be {sorted(expected_totals)} once each (got {cities})")
    elif cities != expected_order:
        problems.append(f"order must be {expected_order} (got {cities})")  # totals alone miss this (Day 18)
    if reply["best_city"] != expected_order[0]:
        problems.append(f"best_city must be {expected_order[0]} (got {reply['best_city']!r})")
    if not isinstance(reply["reason"], str) or not reply["reason"].strip():
        problems.append("reason must be a non-empty sentence")
    return reply, problems


#7 example Day 26: call, check, and save only if every check passed.
reply_text, source = call_llm(system_prompt, user_prompt)
if reply_text is not None:
    reply, problems = validate(reply_text)
    if problems:
        print(f"\nREJECTED reply from {source} -- nothing saved:")
        for problem in problems:
            print(f"  - {problem}")
    else:
        print(f"\nvalidated ranking from {source}:")
        for rank, item in enumerate(reply["ranking"], start=1):
            print(f"  {rank}. {item['city']}: ${item['weekly_total']:,.2f}")
        print(f"best_city: {reply['best_city']}")
        print(f"reason (a human should read this; only the numbers were checked): {reply['reason']}")
        reply["source"] = source  # so the saved file says whether a model or the stub wrote it
        with open(output_name, "w") as file:
            json.dump(reply, file, indent=2)
            file.write("\n")
        print(f"saved {output_name}")

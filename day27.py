import json
import os
import sys  # sys.exit(1) tells whoever ran this script "it failed" (Day 26 always ended with 0)

# Day 27: one strict schema for the LLM ranking, used twice -- sent to the API so the model must
# answer in that shape, and checked again here on EVERY reply (stub included). Then an eval set:
# 5 hand-made replies with a known right verdict, to prove the checker catches what it should.
#
# AI limits (CLAUDE.md): a real call costs money per token; the prompt goes to the provider
# (synthetic offers only); the schema guarantees shape, NOT truth -- the totals are re-checked
# against Python, and a human still reads "reason".

offers = [
    {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
    {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
]
env_name = ".env"
output_name = "llm_ranking.json"
temp_name = output_name + ".tmp"   # written first, moved into place only after validation
eval_name = "eval_results.json"
model_name = "claude-opus-5-5"
timeout_seconds = 30

#1 example Day 27: Python recomputes the totals -- the source of truth every reply is checked against.
for offer in offers:
    offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
expected = sorted(offers, key=lambda offer: offer["weekly_total"], reverse=True)
expected_totals = {offer["city"]: round(offer["weekly_total"], 2) for offer in offers}
expected_order = [offer["city"] for offer in expected]
grand_total = sum(offer["weekly_total"] for offer in offers)

print("recomputed weekly totals:")
for offer in expected:
    print(f"  {offer['city']}: ${offer['weekly_total']:,.2f}")
print(f"grand_total: ${grand_total:,.2f}")
anchor = {"Boston": 3900.00, "Burlington": 3412.00, "Cleveland": 3123.08}
anchor_ok = expected_totals == anchor and round(grand_total, 2) == 10435.08
print(f"matches Day 15 anchor: {anchor_ok}")

#2 example Day 27: the strict schema, written in JSON Schema (the format the API understands).
# "required" = every field must be there; additionalProperties False = no extra fields allowed.
ranking_schema = {
    "type": "object",
    "properties": {
        "ranking": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "weekly_total": {"type": "number"},
                },
                "required": ["city", "weekly_total"],
                "additionalProperties": False,
            },
        },
        "best_city": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": ["ranking", "best_city", "reason"],
    "additionalProperties": False,
}


#3 example Day 27: check a value against the schema. Handles only what this schema uses:
# object, array, string, number. It calls itself for the parts inside (each ranking item).
def check_schema(value, schema, where="reply"):
    kind = schema["type"]
    if kind == "object":
        if not isinstance(value, dict):
            return [f"{where}: expected an object, got {type(value).__name__}"]
        problems = []
        for field in schema["required"]:
            if field not in value:
                problems.append(f"{where}: missing field '{field}'")
        if schema.get("additionalProperties") is False:
            for field in value:
                if field not in schema["properties"]:
                    problems.append(f"{where}: extra field '{field}' is not allowed")
        for field, field_schema in schema["properties"].items():
            if field in value:
                problems += check_schema(value[field], field_schema, f"{where}.{field}")
        return problems
    if kind == "array":
        if not isinstance(value, list):
            return [f"{where}: expected a list, got {type(value).__name__}"]
        problems = []
        for index, item in enumerate(value):
            problems += check_schema(item, schema["items"], f"{where}[{index}]")
        return problems
    if kind == "string":
        return [] if isinstance(value, str) else [f"{where}: expected text, got {value!r}"]
    if kind == "number":
        # bool is excluded on purpose: in Python, True counts as the number 1
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return []
        return [f"{where}: expected a number, got {value!r}"]
    return [f"{where}: schema type '{kind}' is not handled"]


def count_sentences(text):
    # a sentence ends at . ! or ? followed by a space or the end ("$3,123.08" isn't an ending)
    endings = 0
    for index, character in enumerate(text):
        if character in ".!?" and (index == len(text) - 1 or text[index + 1] == " "):
            endings = endings + 1
    return endings


#4 example Day 27: full validation = shape (schema) first, then meaning (checks a schema can't express).
def validate(reply_text):
    try:
        reply = json.loads(reply_text)
    except (TypeError, json.JSONDecodeError) as error:
        return ["not valid JSON (" + str(error) + ")"]
    problems = check_schema(reply, ranking_schema)
    if problems:
        return problems  # the meaning checks below assume the shape is right

    cities = [item["city"] for item in reply["ranking"]]
    if sorted(cities) != sorted(expected_totals):
        problems.append(f"cities must be {sorted(expected_totals)} once each (got {cities})")
    else:
        for item in reply["ranking"]:
            if round(item["weekly_total"], 2) != expected_totals[item["city"]]:
                problems.append(f"{item['city']}: reply says ${item['weekly_total']:,.2f}, "
                                f"Python says ${expected_totals[item['city']]:,.2f}")
        if cities != expected_order:
            problems.append(f"order must be {expected_order} (got {cities})")  # Day 18 lesson
    if cities and reply["best_city"] != cities[0]:
        problems.append(f"best_city {reply['best_city']!r} doesn't match the top-ranked city {cities[0]!r}")
    elif reply["best_city"] != expected_order[0]:
        problems.append(f"best_city must be {expected_order[0]} (got {reply['best_city']!r})")
    if count_sentences(reply["reason"].strip()) != 1:
        problems.append("reason must be exactly one sentence")
    return problems


#5 example Day 27: the Day 26 key + stub path, unchanged except the real call now sends the schema.
def read_env_key(name):
    try:
        with open(env_name, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() == name and value.strip() not in ("", "your_key_here"):
                    return value.strip()
    except FileNotFoundError:
        pass
    return None


def stub_reply():
    # typed by hand from the Day 15 anchor -- NOT built from the recomputed totals (Day 26 lesson)
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


system_prompt = (
    "You rank travel-nurse contract offers by weekly_total = hourly_rate * hours + stipend, "
    "rounded to 2 decimals, highest first. best_city is the top-ranked city. "
    "reason is exactly one plain sentence."
)
user_prompt = "Rank these offers:\n" + "\n".join(
    f"- {offer['city']}: hourly_rate {offer['hourly_rate']}, hours {offer['hours']}, "
    f"stipend {offer['stipend']}"
    for offer in offers
)


def call_llm():
    api_key = read_env_key("LLM_API_KEY")
    if api_key is None:
        print("log: no key found, using stub")
        return stub_reply(), "stub"
    import anthropic  # only needed for a real call, so the stub path runs without it

    client = anthropic.Anthropic(api_key=api_key, timeout=timeout_seconds, max_retries=0)
    try:
        response = client.beta.messages.create(
            model=model_name,
            max_tokens=16000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            # structured output: the API holds the model to this exact shape
            output_config={"effort": "low",
                           "format": {"type": "json_schema", "schema": ranking_schema}},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except anthropic.APITimeoutError:
        print(f"log: no answer within {timeout_seconds} seconds")
        return None, model_name
    except anthropic.APIConnectionError:
        print("log: couldn't reach the API (internet or network blocked)")
        return None, model_name
    except anthropic.AuthenticationError:
        print("log: the key in .env was rejected")
        return None, model_name
    except anthropic.RateLimitError:
        print("log: rate limited -- wait and try again")
        return None, model_name
    except anthropic.APIStatusError as error:
        print(f"log: the API answered with status {error.status_code}")
        return None, model_name
    if response.stop_reason == "refusal":
        print("log: the model declined this request")
        return None, response.model
    text = "".join(block.text for block in response.content if block.type == "text")
    print(f"log: tokens used -- input {response.usage.input_tokens}, output {response.usage.output_tokens}")
    return text, response.model


#6 example Day 27: the eval set -- 5 replies with the verdict a correct checker MUST give.
# This tests the checker, not the model: a real model's answers would be a different eval.
good = json.loads(stub_reply())
def changed(edit):
    reply = json.loads(json.dumps(good))  # a fresh copy, so one case can't leak into the next
    edit(reply)
    return json.dumps(reply)

eval_cases = [
    {"name": "good ranking", "expect": "accept", "reply": json.dumps(good)},
    {"name": "bad JSON", "expect": "reject",
     "reply": '{"ranking": [{"city": "Boston", "weekly_total": 3900'},  # cut off mid-answer
    {"name": "wrong total", "expect": "reject",
     "reply": changed(lambda r: r["ranking"][1].update(weekly_total=3421.00))},  # digits swapped
    {"name": "missing best_city", "expect": "reject",
     "reply": changed(lambda r: r.pop("best_city"))},
    {"name": "best_city not the top-ranked city", "expect": "reject",
     "reply": changed(lambda r: r.update(best_city="Burlington"))},
]

print("\neval set (does the checker give the right verdict?):")
eval_rows = []
for case in eval_cases:
    problems = validate(case["reply"])
    verdict = "reject" if problems else "accept"
    passed = verdict == case["expect"]
    eval_rows.append({"name": case["name"], "expected": case["expect"], "got": verdict,
                      "passed": passed, "problems": problems})
    print(f"  {'PASS' if passed else 'FAIL'}  {case['name']}: expected {case['expect']}, got {verdict}")
    for problem in problems:
        print(f"          - {problem}")
eval_passed = sum(1 for row in eval_rows if row["passed"])
print(f"eval score: {eval_passed}/{len(eval_rows)}")
with open(eval_name, "w") as file:  # no timestamp, so an unchanged result gives an identical file
    json.dump({"score": f"{eval_passed}/{len(eval_rows)}", "passed": eval_passed,
               "total": len(eval_rows), "cases": eval_rows}, file, indent=2)
    file.write("\n")
print(f"saved {eval_name}")

#7 example Day 27: the ranking itself. Saved only if it passes; on any failure the OLD file is
# removed, so nobody mistakes yesterday's good answer for today's (Day 26 open point 1).
reply_text, source = call_llm()
problems = ["no reply (the call failed)"] if reply_text is None else validate(reply_text)
if problems:
    print(f"\nREJECTED reply from {source}:")
    for problem in problems:
        print(f"  - {problem}")
    if os.path.exists(output_name):
        os.remove(output_name)
        print(f"removed the old {output_name} so it can't be mistaken for this run's answer")
else:
    reply = json.loads(reply_text)
    print(f"\nvalidated ranking from {source}:")
    for rank, item in enumerate(reply["ranking"], start=1):
        print(f"  {rank}. {item['city']}: ${item['weekly_total']:,.2f}")
    print(f"best_city: {reply['best_city']}")
    print(f"reason (a human should read this; only the numbers were checked): {reply['reason']}")
    reply["source"] = source
    # write the temp file fully first, then swap it in with one step: os.replace never leaves
    # a half-written llm_ranking.json behind, even if the script is stopped mid-write
    with open(temp_name, "w") as file:
        json.dump(reply, file, indent=2)
        file.write("\n")
    os.replace(temp_name, output_name)
    print(f"saved {output_name}")

#8 example Day 27: exit code -- 0 only if the reply was accepted AND every eval case passed
# (Day 26 open point 2). Anything else exits 1, so a script or a check can tell it failed.
if problems or eval_passed != len(eval_rows) or not anchor_ok:
    print("exit code: 1 (failed)")
    sys.exit(1)
print("exit code: 0 (all good)")

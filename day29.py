import json
import math
import os
import re
import sys
import zlib

import chromadb
from chromadb.config import Settings

# Day 29: RAG step two -- answer a question from retrieved chunks, with citations, and check
# every answer before trusting it. Builds on Day 28's docs/ and Chroma collection; it does NOT
# rebuild them (run `python3 day28.py` first if ./chroma_db is missing).
#
# AI limits (CLAUDE.md): a real call costs money per token; the retrieved chunks are sent to the
# provider (synthetic documents only); and a model can misquote a number or cite the wrong chunk
# while sounding sure -- that's why every number and every citation is checked below.

docs_folder = "docs"
db_folder = "./chroma_db"
collection_name = "contract_docs"
eval_name = "qa_eval.json"
env_name = ".env"
model_name = "claude-opus-5-5"
timeout_seconds = 30
top_k = 3               # how many chunks are given to the answerer as context
min_coverage = 0.5      # same confidence rule as Day 28
dont_know = "I don't know — not in the documents"
citation_pattern = re.compile(r"\[([\w.-]+\.md), chunk (\d+)\]")   # [boston_offer.md, chunk 1]
number_pattern = re.compile(r"\$?\d[\d,]*(?:\.\d+)?")

# Day 15 anchor, by document (each document is one city's offer).
anchor = {"boston_offer.md": 3900.00, "burlington_offer.md": 3412.00, "cleveland_offer.md": 3123.08}
anchor_grand_total = 10435.08

#1 example Day 29: the Day 28 word-overlap STUB embedding, copied word for word.
# It can't be imported: importing day28.py would run it and rebuild the collection. A copy can
# drift from the original, so #2 below re-embeds every stored chunk and compares the vectors.
dimensions = 1024
stop_words = {"a", "an", "and", "are", "as", "at", "be", "by", "do", "does", "for", "from", "has",
              "how", "if", "in", "is", "it", "its", "much", "not", "of", "on", "or", "the", "that",
              "this", "to", "what", "when", "where", "which", "who", "with"}


def key_words(text):
    words = set()
    for word in re.findall(r"\$?\d[\d,]*(?:\.\d+)?|[a-z]+", text.lower()):
        word = word.replace("$", "").replace(",", "")
        if word in stop_words:
            continue
        if (word.isalpha() and len(word) > 3 and word.endswith("s")
                and not word.endswith(("ss", "us"))):
            word = word[:-1]
        words.add(word)
    return words


def stub_embed(text):
    """STUB embedding (same as Day 28): key words hashed into 1024 slots, scaled to length 1."""
    vector = [0.0] * dimensions
    for word in key_words(text):
        vector[zlib.crc32(word.encode()) % dimensions] = 1.0
    length = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / length for value in vector]


#2 example Day 29: load the existing collection and check it before using it.
if not os.path.isdir(db_folder):
    print(f"{db_folder} not found -- run `python3 day28.py` first to build the collection")
    sys.exit(1)
client = chromadb.PersistentClient(path=db_folder, settings=Settings(anonymized_telemetry=False))
try:
    collection = client.get_collection(collection_name)
except Exception as error:  # Chroma raises its own "not found" error type
    print(f"collection '{collection_name}' not found ({type(error).__name__}) -- run `python3 day28.py` first")
    sys.exit(1)

stored = collection.get(include=["documents", "metadatas", "embeddings"])
setup_problems = []
per_doc = {}
for text, metadata, vector in zip(stored["documents"], stored["metadatas"], stored["embeddings"]):
    source = metadata.get("source")
    per_doc[source] = per_doc.get(source, 0) + 1
    if "chunk_index" not in metadata:
        setup_problems.append(f"{source}: chunk without a chunk_index")
    if len(text) > 520:  # "about 500 characters" (a cut moves back to a space or paragraph break)
        setup_problems.append(f"{source}: a chunk is {len(text)} characters")
    with open(os.path.join(docs_folder, source), "r") as file:
        if text not in file.read():  # chunk must still be word for word in today's document
            setup_problems.append(f"{source} #{metadata.get('chunk_index')}: text no longer in the document")
    # length first: zip() stops at the shorter list, so a 384-number vector (day30.py's real model)
    # would otherwise be compared with only the first 384 of our 1024 numbers
    if len(vector) != dimensions:
        setup_problems.append(f"{source} #{metadata.get('chunk_index')}: stored vector has {len(vector)} numbers, "
                              f"this file's stub_embed makes {dimensions} (another embedding built the collection)")
    elif max(abs(a - b) for a, b in zip(vector, stub_embed(text))) > 1e-6:
        setup_problems.append(f"{source} #{metadata.get('chunk_index')}: stored vector != this file's stub_embed")
print(f"loaded {collection.count()} chunks from {db_folder}, collection '{collection_name}':")
for source in sorted(per_doc):
    print(f"  {source}: {per_doc[source]} chunks")
print(f"collection matches docs/ and the embedding: {not setup_problems}")
for problem in setup_problems:
    print(f"  - {problem}")
if setup_problems:
    # Stop here: querying a collection built differently crashed with a traceback (found on Day 30).
    # Exiting before the eval also leaves the saved qa_eval.json untouched.
    print("the collection doesn't match what day29.py expects -- run `python3 day28.py` to rebuild it, then try again")
    print("exit code: 1 (failed)")
    sys.exit(1)


#3 example Day 29: retrieve the top 3 chunks. Confidence = Day 28's rule on the top chunk.
def retrieve(question):
    asked = key_words(question)
    if not asked:  # empty or only filler words: nothing to search for
        return [], False
    # Ask Chroma for every chunk (only 8 here), then sort ourselves: Chroma returns TIED chunks in
    # a random order, which made qa_eval.json change between identical runs. Ties are broken by
    # file name, then chunk number. Chunks sharing no word with the question (similarity 0) are
    # dropped: they're noise, and noise in the context invites a confused answer.
    result = collection.query(query_embeddings=[stub_embed(question)], n_results=collection.count(),
                              include=["documents", "metadatas", "distances"])
    chunks = []
    for text, metadata, distance in zip(result["documents"][0], result["metadatas"][0],
                                        result["distances"][0]):
        similarity = round(1 - distance, 4)
        if similarity <= 0:
            continue
        chunks.append({"source": metadata["source"], "chunk": metadata["chunk_index"], "text": text,
                       "similarity": similarity,
                       "coverage": round(len(asked & key_words(text)) / len(asked), 4)})
    chunks.sort(key=lambda chunk: (-chunk["similarity"], chunk["source"], chunk["chunk"]))
    chunks = chunks[:top_k]
    return chunks, bool(chunks) and chunks[0]["coverage"] >= min_coverage


def label(chunk):
    return f"[{chunk['source']}, chunk {chunk['chunk']}]"


#4 example Day 29: the prompt -- ONLY the retrieved chunks, each with its citation label.
def build_prompt(question, chunks):
    system_text = (
        "Answer the question using ONLY the context chunks below. Do not use outside knowledge. "
        "After every fact, cite the chunk it came from exactly like this: [filename.md, chunk N]. "
        "Copy every number exactly as it is written in the chunk. "
        f"If the chunks don't contain the answer, reply exactly: {dont_know}"
    )
    context = "\n\n".join(f"{label(chunk)}\n{chunk['text']}" for chunk in chunks)
    user_text = f"Context chunks:\n\n{context}\n\nQuestion: {question}"
    return system_text, user_text


#5 example Day 29: the answerer. Stub first: with no key, the answer is the single sentence from
# the retrieved chunks that shares the most key words with the question, quoted with its
# citation -- every word comes from a chunk, nothing is invented.
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


def stub_answer(question, chunks):
    asked = key_words(question)
    best_sentence, best_chunk, best_score = None, None, 0
    for chunk in chunks:  # chunks arrive best-first, so a tie keeps the higher-ranked chunk
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", chunk["text"]):
            score = len(asked & key_words(sentence))
            if score > best_score:
                best_sentence, best_chunk, best_score = sentence.strip(), chunk, score
    if best_sentence is None:
        return dont_know
    return f"From {best_chunk['source']}: \"{best_sentence}\" {label(best_chunk)}"


def call_llm(question, chunks):
    api_key = read_env_key("LLM_API_KEY")
    if api_key is None:
        return stub_answer(question, chunks), "stub"
    import anthropic  # only needed for a real call

    system_text, user_text = build_prompt(question, chunks)
    client_llm = anthropic.Anthropic(api_key=api_key, timeout=timeout_seconds, max_retries=0)
    try:
        response = client_llm.beta.messages.create(
            model=model_name, max_tokens=16000, system=system_text,
            messages=[{"role": "user", "content": user_text}],
            output_config={"effort": "low"},
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
        )
    except anthropic.APITimeoutError:
        print(f"  log: no answer within {timeout_seconds} seconds")
        return None, model_name
    except anthropic.APIConnectionError:
        print("  log: couldn't reach the API")
        return None, model_name
    except anthropic.AuthenticationError:
        print("  log: the key in .env was rejected")
        return None, model_name
    except anthropic.APIStatusError as error:
        print(f"  log: the API answered with status {error.status_code}")
        return None, model_name
    if response.stop_reason == "refusal":
        print("  log: the model declined this request")
        return None, response.model
    return "".join(b.text for b in response.content if b.type == "text").strip(), response.model


#6 example Day 29: check an answer. Every citation must name a chunk that was retrieved; every
# number must appear in the chunk(s) its sentence cites; a weekly total must equal the anchor
# for the city of the document it cites. An empty list means the answer passed.
def money(text):
    return {round(float(n.replace("$", "").replace(",", "")), 2) for n in number_pattern.findall(text)}


def validate(answer, chunks, confident):
    if answer is None:
        return ["no answer (the call failed)"]
    if not confident:
        return [] if answer == dont_know else [f"retrieval was not confident, so the answer must be exactly '{dont_know}'"]
    if answer == dont_know:
        return []  # declining is always allowed; the eval decides whether it was the right call
    problems = []
    retrieved = {(chunk["source"], chunk["chunk"]): chunk for chunk in chunks}
    # split into "facts": each piece of text ends with its citation(s)
    pieces = re.split(r"(?<=\])\s*(?=[^\[\s])", answer)
    cited_any = False
    for piece in pieces:
        cites = [(source, int(number)) for source, number in citation_pattern.findall(piece)]
        text_only = citation_pattern.sub("", piece)
        numbers = money(text_only)
        if not cites:
            if numbers:
                problems.append(f"uncited number(s) {sorted(numbers)} in: {text_only.strip()!r}")
            continue
        cited_any = True
        missing = [c for c in cites if c not in retrieved]
        for source, number in missing:
            problems.append(f"cites [{source}, chunk {number}], which was not retrieved")
        cited_chunks = [retrieved[c] for c in cites if c in retrieved]
        in_chunks = set().union(*(money(c["text"]) for c in cited_chunks)) if cited_chunks else set()
        for value in sorted(numbers - in_chunks):
            problems.append(f"${value:,.2f} is not in the cited chunk(s)")
        if "weekly total" in text_only.lower():
            for chunk in cited_chunks:
                expected = anchor[chunk["source"]]
                other_cities = numbers & (set(anchor.values()) - {expected})
                if expected not in numbers or other_cities:
                    problems.append(f"weekly total for {chunk['source']} must be ${expected:,.2f} (anchor)")
    if not cited_any:
        problems.append("no citation at all")
    return problems


#7 example Day 29: the whole pipeline for one question.
def ask(question):
    chunks, confident = retrieve(question)
    if not confident:
        answer, source = dont_know, "rule"  # no guessed number, no citation
    else:
        answer, source = call_llm(question, chunks)
    problems = validate(answer, chunks, confident)
    print(f"\nQ: {question}")
    for chunk in chunks:
        print(f"  retrieved {label(chunk)} similarity {chunk['similarity']:.3f} coverage {chunk['coverage']:.0%}")
    if problems:
        print(f"  REJECTED answer from {source} -- nothing saved:")
        for problem in problems:
            print(f"    - {problem}")
        return None, chunks, problems, source
    print(f"  A ({source}): {answer}")
    return answer, chunks, problems, source


#8 example Day 29: the 5-question eval.
eval_cases = [
    {"question": "Which city pays $3,900.00?", "expect": {"amount": 3900.00, "source": "boston_offer.md"}},
    {"question": "Which city pays $3,412.00?", "expect": {"amount": 3412.00, "source": "burlington_offer.md"}},
    {"question": "Which city pays $3,123.08?", "expect": {"amount": 3123.08, "source": "cleveland_offer.md"}},
    {"question": "Which offer pays a completion bonus, and how much is it?",
     "expect": {"amount": 1000.00, "source": "burlington_offer.md"}},
    {"question": "What is the signing bonus in Miami?", "expect": {"dont_know": True}},
]
rows = []
for case in eval_cases:
    answer, chunks, problems, source = ask(case["question"])
    expect = case["expect"]
    if expect.get("dont_know"):
        passed = answer == dont_know
    else:
        cited = {s for s, n in citation_pattern.findall(answer or "")}
        passed = (answer is not None and answer != dont_know and expect["amount"] in money(
            citation_pattern.sub("", answer)) and expect["source"] in cited)
    rows.append({"question": case["question"], "expected": expect, "answer": answer,
                 "answered_by": source, "rejected_because": problems,
                 "retrieved": [label(chunk) for chunk in chunks], "passed": passed})
score = sum(1 for row in rows if row["passed"])

# Grand total read OUT OF the three validated weekly-total answers (not from the expected values,
# which would make this check circular). Each answer must hold exactly one weekly-total-sized number.
city_totals = []
for row in rows[:3]:
    amounts = [v for v in money(citation_pattern.sub("", row["answer"] or "")) if v >= 1000]
    if row["passed"] and len(amounts) == 1:
        city_totals.append(amounts[0])
grand_total = round(sum(city_totals), 2)
grand_ok = len(city_totals) == 3 and grand_total == anchor_grand_total

print(f"\nQA eval: {score}/{len(rows)}")
for row in rows:
    print(f"  {'PASS' if row['passed'] else 'FAIL'}  {row['question']}")
print(f"grand total from the 3 answered weekly totals: ${grand_total:,.2f} (anchor $10,435.08): {grand_ok}")

with open(eval_name, "w") as file:   # no timestamp, so the same result gives an identical file
    json.dump({"score": f"{score}/{len(rows)}", "passed": score, "total": len(rows),
               "grand_total_from_answers": grand_total, "grand_total_matches_anchor": grand_ok,
               "top_k": top_k, "confidence_rule": f"top chunk covers >= {min_coverage:.0%} of the question's key words",
               "cases": rows}, file, indent=2, ensure_ascii=False)
    file.write("\n")
print(f"saved {eval_name}")

#9 example Day 29: exit 1 if anything failed (Day 27 habit).
if score != len(rows) or not grand_ok or setup_problems:
    print("exit code: 1 (failed)")
    sys.exit(1)
print("exit code: 0 (all good)")

import json
import math
import os
import re
import shutil
import sys
import zlib

import chromadb                       # vector database: stores chunks + their vectors, finds the nearest
from chromadb.config import Settings

# Day 28: RAG step one -- retrieval. Split documents into chunks, turn each chunk into a vector,
# store them in Chroma, and for a question find the chunk(s) most like it.
# No API key and no paid call: the embedding below is a STUB that only compares words.
# Limits: a real embedding model understands meaning ("pay" ~ "salary"); this stub only counts
# shared words, so it would miss a question asked in different words. All documents are synthetic.

docs_folder = "docs"
doc_names = ["boston_offer.md", "burlington_offer.md", "cleveland_offer.md"]
db_folder = "./chroma_db"
collection_name = "contract_docs"
eval_name = "rag_eval.json"
chunk_size = 500        # about 500 characters per chunk
chunk_overlap = 50      # about 50 characters repeated at the start of the next chunk
min_coverage = 0.5      # at least half of the question's key words must be in the top chunk
dimensions = 1024       # length of each stub vector

#1 example Day 28: the same 3 synthetic offers, so each document can be checked against the anchor.
offers = {
    "boston_offer.md": {"city": "Boston", "hourly_rate": 35, "stipend": 2500, "hours": 40},
    "burlington_offer.md": {"city": "Burlington", "hourly_rate": 42, "stipend": 1900, "hours": 36},
    "cleveland_offer.md": {"city": "Cleveland", "hourly_rate": 39.53, "stipend": 1700, "hours": 36},
}
anchor_ok = True
for name, offer in offers.items():
    offer["weekly_total"] = offer["hourly_rate"] * offer["hours"] + offer["stipend"]
grand_total = sum(offer["weekly_total"] for offer in offers.values())


#2 example Day 28: split text into ~500-character chunks with ~50 characters of overlap.
# Where to cut matters more than the size. A plain 500-character cut split Cleveland's
# "weekly total is $3,123.08 ... in hourly pay" across two chunks, so neither chunk held the
# whole fact and the eval failed (2/3). Fix: cut at a paragraph break ("\n\n") when there is one
# in the second half of the window -- a paragraph is one idea -- otherwise at a space.
def split_into_chunks(text):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            paragraph_break = text.rfind("\n\n", start + chunk_size // 2, end)
            space = text.rfind(" ", start, end)
            if paragraph_break != -1:
                end = paragraph_break  # keep each paragraph (one idea) whole
            elif space > start:
                end = space            # at least don't cut "$3,900.00" in half
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        next_start = end - chunk_overlap
        space = text.find(" ", next_start, end)
        next_start = space + 1 if space != -1 else next_start  # start the overlap on a whole word
        start = next_start if next_start > start else end      # always move forward (no endless loop)
    return chunks


print("documents (each checked against the Day 15 anchor):")
all_chunks = []   # one dict per chunk: id, text, and metadata (source file + chunk index)
for name in doc_names:
    with open(os.path.join(docs_folder, name), "r") as file:
        text = file.read()
    total_text = f"${offers[name]['weekly_total']:,.2f}"
    found = total_text in text
    anchor_ok = anchor_ok and found
    pieces = split_into_chunks(text)
    for index, piece in enumerate(pieces):
        all_chunks.append({"id": f"{name}#{index}", "text": piece,
                           "metadata": {"source": name, "chunk_index": index}})
    print(f"  {name}: {len(text)} characters -> {len(pieces)} chunks | "
          f"weekly total {total_text} in the text: {found}")
print(f"total chunks: {len(all_chunks)}")
print(f"grand_total of the 3 weekly totals: ${grand_total:,.2f}")

#3 example Day 28: the STUB embedding -- word overlap only, deterministic, free.
# "Stop words" (the, is, which...) are dropped so they don't count as a match.
stop_words = {"a", "an", "and", "are", "as", "at", "be", "by", "do", "does", "for", "from", "has",
              "how", "if", "in", "is", "it", "its", "much", "not", "of", "on", "or", "the", "that",
              "this", "to", "what", "when", "where", "which", "who", "with"}


def key_words(text):
    words = set()
    # a money amount stays one word ("$3,900.00" -> "3900.00"); other words are lower-cased letters
    for word in re.findall(r"\$?\d[\d,]*(?:\.\d+)?|[a-z]+", text.lower()):
        word = word.replace("$", "").replace(",", "")
        if word in stop_words:
            continue
        if (word.isalpha() and len(word) > 3 and word.endswith("s")
                and not word.endswith(("ss", "us"))):
            word = word[:-1]   # crude plural trim: "pays" -> "pay", "hours" -> "hour" ("bonus" stays)
        words.add(word)
    return words


def stub_embed(text):
    """STUB embedding (not a real model): each key word switches on one of 1024 slots.
    zlib.crc32 picks the slot -- the same word always lands in the same slot (Python's own
    hash() changes between runs, so it can't be used). Scaled to length 1, so Chroma's
    cosine similarity becomes "shared words / sqrt(words in A x words in B)"."""
    vector = [0.0] * dimensions
    for word in key_words(text):
        vector[zlib.crc32(word.encode()) % dimensions] = 1.0
    length = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / length for value in vector]


#4 example Day 28: store every chunk in Chroma. The folder is rebuilt from scratch each run,
# so re-running can't add the same chunks twice (the Day 21 double-count lesson).
if os.path.exists(db_folder):
    shutil.rmtree(db_folder)
client = chromadb.PersistentClient(path=db_folder,
                                   settings=Settings(anonymized_telemetry=False))  # no usage data sent
collection = client.create_collection(
    name=collection_name,
    embedding_function=None,                       # we give our own vectors; nothing is downloaded
    configuration={"hnsw": {"space": "cosine"}},   # distance = 1 - cosine similarity
)
collection.add(
    ids=[chunk["id"] for chunk in all_chunks],
    documents=[chunk["text"] for chunk in all_chunks],
    metadatas=[chunk["metadata"] for chunk in all_chunks],
    embeddings=[stub_embed(chunk["text"]) for chunk in all_chunks],
)
print(f"stored {collection.count()} chunks in {db_folder}, collection '{collection_name}'")


#5 example Day 28: retrieve. Chroma ranks by similarity; "coverage" decides confidence:
# the share of the question's key words that really appear in the top chunk.
def retrieve(question, how_many=2):
    result = collection.query(query_embeddings=[stub_embed(question)], n_results=how_many,
                              include=["documents", "metadatas", "distances"])
    hits = []
    for text, metadata, distance in zip(result["documents"][0], result["metadatas"][0],
                                        result["distances"][0]):
        asked = key_words(question)
        coverage = len(asked & key_words(text)) / len(asked) if asked else 0.0
        hits.append({"text": text, "source": metadata["source"],
                     "chunk_index": metadata["chunk_index"],
                     "similarity": round(1 - distance, 4), "coverage": round(coverage, 4)})
    return hits


def answer(question):
    hits = retrieve(question)
    top = hits[0]
    confident = top["coverage"] >= min_coverage
    print(f"\nQ: {question}")
    if not confident:
        print(f"  best match {top['source']} #{top['chunk_index']} only covers "
              f"{top['coverage']:.0%} of the key words {sorted(key_words(question))}")
        print("  I don't know — not in the documents")
    else:
        for rank, hit in enumerate(hits, start=1):
            print(f"  {rank}. {hit['source']} #{hit['chunk_index']} | similarity {hit['similarity']:.3f}"
                  f" | coverage {hit['coverage']:.0%}")
        print(f"  top chunk text:\n    " + top["text"].replace("\n", "\n    "))
    return top, confident


#6 example Day 28: retrieval eval -- does the top-1 chunk come from the right document?
eval_cases = [
    {"question": "Which city pays $3,900.00?", "expected_source": "boston_offer.md"},
    {"question": "Which city pays $3,412.00?", "expected_source": "burlington_offer.md"},
    {"question": "Which city pays $3,123.08?", "expected_source": "cleveland_offer.md"},
]
eval_rows = []
for case in eval_cases:
    top, confident = answer(case["question"])
    passed = confident and top["source"] == case["expected_source"]
    eval_rows.append({"question": case["question"], "expected_source": case["expected_source"],
                      "top1_source": top["source"], "top1_chunk_index": top["chunk_index"],
                      "similarity": top["similarity"], "coverage": top["coverage"],
                      "confident": confident, "passed": passed})
score = sum(1 for row in eval_rows if row["passed"])
print(f"\nretrieval eval: {score}/{len(eval_rows)} top-1 from the correct document")
for row in eval_rows:
    print(f"  {'PASS' if row['passed'] else 'FAIL'}  {row['question']} -> {row['top1_source']}")

#7 example Day 28: a question the documents can't answer must NOT get a confident hit.
miami_question = "What is the signing bonus in Miami?"
miami_top, miami_confident = answer(miami_question)
unknown_ok = not miami_confident

with open(eval_name, "w") as file:   # no timestamp, so the same result gives an identical file
    json.dump({
        "embedding": "STUB word-overlap: crc32-hashed key words, 1024 dims, no model, no API",
        "chunking": {"size": chunk_size, "overlap": chunk_overlap, "total_chunks": len(all_chunks)},
        "confidence_rule": f"top chunk must contain at least {min_coverage:.0%} of the question's key words",
        "score": f"{score}/{len(eval_rows)}", "passed": score, "total": len(eval_rows),
        "cases": eval_rows,
        "unanswerable": {"question": miami_question, "top1_source": miami_top["source"],
                         "similarity": miami_top["similarity"], "coverage": miami_top["coverage"],
                         "confident": miami_confident, "passed": unknown_ok},
    }, file, indent=2)
    file.write("\n")
print(f"\nsaved {eval_name}")

#8 example Day 28: exit 1 if anything failed, so a script or check can tell (Day 27 habit).
if score != len(eval_rows) or not unknown_ok or not anchor_ok:
    print("exit code: 1 (failed)")
    sys.exit(1)
print("exit code: 0 (all good)")

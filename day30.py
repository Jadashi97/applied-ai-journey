import ast
import json
import math
import os
import re
import shutil
import sys
import zlib

import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

# Day 30: swap the Day 28 STUB embedding (shared words only) for a REAL embedding model and
# re-run both evals. Only the embedding changes -- chunking, the confidence rule, the answerer
# and the answer checker are loaded from day28.py / day29.py, so any score change comes from
# the embedding.
#
# The model: Chroma's default, all-MiniLM-L6-v2 (384 numbers per text), run by onnxruntime on
# THIS machine. Free, no API key, no paid call. The first run downloads it once (~80 MB, cached
# in ~/.cache/chroma); after that it runs with no network, so document text never leaves the
# machine. Limits: it's small and general-purpose -- good at meaning ("pay" ~ "salary"), weak
# at telling numbers apart. That matters here, because the eval questions are about numbers.

day28_file, day29_file = "day28.py", "day29.py"
docs_folder = "docs"
db_folder = "./chroma_db"
collection_name = "contract_docs"
doc_names = ["boston_offer.md", "burlington_offer.md", "cleveland_offer.md"]
stub_retrieval_file, stub_qa_file = "rag_eval.json", "qa_eval.json"   # committed stub results
output_name = "real_embeddings_eval.json"
model_label = "all-MiniLM-L6-v2 (Chroma DefaultEmbeddingFunction, local ONNX)"


#1 example Day 30: borrow exact definitions from day28.py and day29.py WITHOUT running them
# (running them would rebuild or require the stub collection). `ast` reads a .py file as a tree;
# we keep only the named functions and settings and run just those lines.
def load_definitions(file_name, names):
    with open(file_name, "r") as file:
        tree = ast.parse(file.read())
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            keep.append(node)
        elif isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id in names for target in node.targets):
            keep.append(node)
    namespace = {"re": re, "math": math, "zlib": zlib}
    exec(compile(ast.Module(body=keep, type_ignores=[]), file_name, "exec"), namespace)
    missing = [name for name in names if name not in namespace]
    if missing:
        sys.exit(f"{file_name} no longer defines {missing} -- day30.py needs updating")
    return namespace


day28 = load_definitions(day28_file, ["chunk_size", "chunk_overlap", "split_into_chunks"])
day29 = load_definitions(day29_file, [
    "stop_words", "key_words", "label", "money", "validate", "stub_answer", "dont_know",
    "citation_pattern", "number_pattern", "anchor", "anchor_grand_total", "top_k", "min_coverage"])
key_words, label, money = day29["key_words"], day29["label"], day29["money"]
validate, stub_answer, dont_know = day29["validate"], day29["stub_answer"], day29["dont_know"]
citation_pattern, anchor, top_k, min_coverage = (day29["citation_pattern"], day29["anchor"],
                                                 day29["top_k"], day29["min_coverage"])

#2 example Day 30: same docs, same chunking (from day28.py), each checked against the anchor.
all_chunks, anchor_ok = [], True
print("documents (same chunking as Day 28):")
for name in doc_names:
    with open(os.path.join(docs_folder, name), "r") as file:
        text = file.read()
    found = f"${anchor[name]:,.2f}" in text
    anchor_ok = anchor_ok and found
    pieces = day28["split_into_chunks"](text)
    for index, piece in enumerate(pieces):
        all_chunks.append({"id": f"{name}#{index}", "text": piece,
                           "metadata": {"source": name, "chunk_index": index}})
    print(f"  {name}: {len(pieces)} chunks | weekly total ${anchor[name]:,.2f} in the text: {found}")
print(f"total chunks: {len(all_chunks)} | grand total of the anchors: ${sum(anchor.values()):,.2f}")

#3 example Day 30: rebuild contract_docs with the REAL embedding. Chroma now turns each chunk's
# text into a vector itself (embedding_function=...), instead of us passing stub vectors.
if os.path.exists(db_folder):
    shutil.rmtree(db_folder)
client = chromadb.PersistentClient(path=db_folder, settings=Settings(anonymized_telemetry=False))
collection = client.create_collection(name=collection_name, embedding_function=DefaultEmbeddingFunction(),
                                      configuration={"hnsw": {"space": "cosine"}})
collection.add(ids=[c["id"] for c in all_chunks], documents=[c["text"] for c in all_chunks],
               metadatas=[c["metadata"] for c in all_chunks])
print(f"stored {collection.count()} chunks with real embeddings in {db_folder}, collection '{collection_name}'")
print("  note: day29.py checks for STUB vectors, so it will report a mismatch until `python3 day28.py` is re-run")


#4 example Day 30: retrieval -- same rules as Day 29 (fixed tie-break, top 3, Day 28 confidence
# rule on the top chunk), only the vectors are different.
def retrieve(question):
    asked = key_words(question)
    if not asked:
        return [], False, []
    result = collection.query(query_texts=[question], n_results=collection.count(),
                              include=["documents", "metadatas", "distances"])
    ranked = []
    for text, metadata, distance in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        ranked.append({"source": metadata["source"], "chunk": metadata["chunk_index"], "text": text,
                       "similarity": round(1 - distance, 4),
                       "coverage": round(len(asked & key_words(text)) / len(asked), 4)})
    ranked.sort(key=lambda c: (-c["similarity"], c["source"], c["chunk"]))
    chunks = [c for c in ranked if c["similarity"] > 0][:top_k]
    return chunks, bool(chunks) and chunks[0]["coverage"] >= min_coverage, ranked


def doc_rank(ranked, source):
    # 1 = the right document's best chunk is the top result
    for position, chunk in enumerate(ranked, start=1):
        if chunk["source"] == source:
            return position
    return None


#5 example Day 30: the Day 28 retrieval eval and the Day 29 Q&A eval, real embeddings.
with open(stub_retrieval_file) as file:
    stub_retrieval = {case["question"]: case for case in json.load(file)["cases"]}
with open(stub_qa_file) as file:
    stub_qa = {case["question"]: case for case in json.load(file)["cases"]}

retrieval_questions = [("Which city pays $3,900.00?", "boston_offer.md"),
                       ("Which city pays $3,412.00?", "burlington_offer.md"),
                       ("Which city pays $3,123.08?", "cleveland_offer.md")]
qa_cases = [("Which city pays $3,900.00?", {"amount": 3900.00, "source": "boston_offer.md"}),
            ("Which city pays $3,412.00?", {"amount": 3412.00, "source": "burlington_offer.md"}),
            ("Which city pays $3,123.08?", {"amount": 3123.08, "source": "cleveland_offer.md"}),
            ("Which offer pays a completion bonus, and how much is it?",
             {"amount": 1000.00, "source": "burlington_offer.md"}),
            ("What is the signing bonus in Miami?", {"dont_know": True})]

print("\n=== retrieval eval (Day 28 questions): top-1 from the correct document, confident")
retrieval_rows = []
for question, expected in retrieval_questions:
    chunks, confident, ranked = retrieve(question)
    top = chunks[0] if chunks else None
    passed = bool(top) and confident and top["source"] == expected
    stub = stub_retrieval[question]
    retrieval_rows.append({
        "question": question, "expected_source": expected, "passed": passed,
        "real": {"top1": label(top) if top else None, "similarity": top and top["similarity"],
                 "coverage": top and top["coverage"], "rank_of_correct_doc": doc_rank(ranked, expected),
                 "runner_up": label(ranked[1]) if len(ranked) > 1 else None,
                 "runner_up_similarity": ranked[1]["similarity"] if len(ranked) > 1 else None},
        "stub": {"top1": f"[{stub['top1_source']}, chunk {stub['top1_chunk_index']}]",
                 "similarity": stub["similarity"], "passed": stub["passed"]}})
    print(f"  {'PASS' if passed else 'FAIL'}  {question} -> {label(top) if top else 'nothing'} "
          f"similarity {top['similarity'] if top else 0:.3f} (runner-up {ranked[1]['similarity']:.3f}) | "
          f"stub: {retrieval_rows[-1]['stub']['top1']} {'PASS' if stub['passed'] else 'FAIL'}")
retrieval_score = sum(r["passed"] for r in retrieval_rows)
print(f"retrieval eval: {retrieval_score}/{len(retrieval_rows)}  (stub: "
      f"{sum(r['stub']['passed'] for r in retrieval_rows)}/{len(retrieval_rows)})")

print("\n=== Q&A eval (Day 29 questions, Day 29 answerer and checker)")
qa_rows = []
for question, expected in qa_cases:
    chunks, confident, ranked = retrieve(question)
    answer = stub_answer(question, chunks) if confident else dont_know
    problems = validate(answer, chunks, confident)
    if problems:
        answer = None  # rejected answers are not kept
    if expected.get("dont_know"):
        passed = answer == dont_know
    else:
        cited = {s for s, n in citation_pattern.findall(answer or "")}
        passed = (answer not in (None, dont_know) and expected["amount"] in money(citation_pattern.sub("", answer))
                  and expected["source"] in cited)
    stub = stub_qa[question]
    qa_rows.append({"question": question, "expected": expected, "passed": passed, "answer": answer,
                    "rejected_because": problems,
                    "real_retrieved": [f"{label(c)} {c['similarity']:.3f}" for c in chunks],
                    "real_top_similarity": chunks[0]["similarity"] if chunks else None,
                    "stub": {"answer": stub["answer"], "passed": stub["passed"]}})
    print(f"  {'PASS' if passed else 'FAIL'}  {question}\n        real: {answer}")
    if answer != stub["answer"]:
        print(f"        stub: {stub['answer']}")
qa_score = sum(r["passed"] for r in qa_rows)
city_totals = [v for r in qa_rows[:3] if r["passed"]
               for v in money(citation_pattern.sub("", r["answer"])) if v >= 1000]
grand_total = round(sum(city_totals), 2)
print(f"Q&A eval: {qa_score}/{len(qa_rows)}  (stub: {sum(r['stub']['passed'] for r in qa_rows)}/{len(qa_rows)})"
      f" | grand total from answers ${grand_total:,.2f}")

#6 example Day 30: findings -- every question where the real embedding did WORSE than the stub,
# plus what the similarity numbers show. Logged, not hidden.
findings = []
for row in retrieval_rows:
    if row["stub"]["passed"] and not row["passed"]:
        findings.append(f"WORSE (retrieval): '{row['question']}' -- stub passed with {row['stub']['top1']}, "
                        f"real top-1 is {row['real']['top1']}; correct document ranked {row['real']['rank_of_correct_doc']}")
    elif row["real"]["top1"] != row["stub"]["top1"]:
        findings.append(f"changed (retrieval): '{row['question']}' -- top-1 moved from {row['stub']['top1']} "
                        f"to {row['real']['top1']}, still {'PASS' if row['passed'] else 'FAIL'}")
for row in qa_rows:
    if row["stub"]["passed"] and not row["passed"]:
        findings.append(f"WORSE (Q&A): '{row['question']}' -- stub answer passed, real answer: {row['answer']!r}"
                        + (f", rejected because {row['rejected_because']}" if row["rejected_because"] else ""))
# Safety: a failure can be a refusal ("I don't know") or a WRONG answer. Only the second is dangerous.
wrong_answers = [r["question"] for r in qa_rows if not r["passed"] and r["answer"] not in (None, dont_know)]
refusals = [r["question"] for r in qa_rows if not r["passed"] and r["answer"] == dont_know]
findings.append(f"safety: {len(wrong_answers)} wrong answer(s) given; {len(refusals)} failure(s) were "
                f"'I don't know' refusals -- the word-coverage rule stopped a wrong document from being "
                f"quoted" if refusals and not wrong_answers else
                f"safety: {len(wrong_answers)} wrong answer(s) given: {wrong_answers}")
answerable = [r["real_top_similarity"] for r in qa_rows if not r["expected"].get("dont_know")]
miami = qa_rows[-1]["real_top_similarity"]
findings.append(f"similarity gap: answerable questions' top similarity {min(answerable):.3f}-{max(answerable):.3f}; "
                f"Miami's top similarity {miami:.3f} -- "
                + ("a similarity threshold alone COULD separate them" if miami < min(answerable)
                   else "a similarity threshold alone could NOT separate them; the word-coverage rule is what says 'I don't know'"))
margins = [r["real"]["similarity"] - r["real"]["runner_up_similarity"] for r in retrieval_rows]
findings.append(f"number questions: real top-1 beats the runner-up by only {min(margins):.3f}-{max(margins):.3f} "
                f"similarity -- the model barely tells $3,900.00 from $3,412.00 (stub margins were ~0.09)")
print("\n=== findings")
for finding in findings:
    print(f"  - {finding}")

with open(output_name, "w") as file:  # no timestamp; rounded, so an unchanged result gives an identical file
    json.dump({"embedding": model_label, "dimensions": 384,
               "same_as_stub_runs": "docs, chunking, top_k, confidence rule, answerer, checker",
               "total_chunks": collection.count(), "anchor_totals_in_docs": anchor_ok,
               "retrieval": {"score": f"{retrieval_score}/{len(retrieval_rows)}", "passed": retrieval_score,
                             "total": len(retrieval_rows), "cases": retrieval_rows},
               "qa": {"score": f"{qa_score}/{len(qa_rows)}", "passed": qa_score, "total": len(qa_rows),
                      "grand_total_from_answers": grand_total, "cases": qa_rows},
               "findings": findings}, file, indent=2, ensure_ascii=False)
    file.write("\n")
print(f"\nsaved {output_name}")

#7 example Day 30: exit 1 if a target was missed (3/3, 5/5, $10,435.08), so the miss can't be overlooked.
if retrieval_score != 3 or qa_score != 5 or grand_total != day29["anchor_grand_total"] or not anchor_ok:
    print("exit code: 1 (a target was missed -- see findings)")
    sys.exit(1)
print("exit code: 0 (all targets met)")

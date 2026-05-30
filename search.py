# search.py — Ricerca semantica locale sulla KB (zero token cloud)
# Requisiti: pip install chromadb sentence-transformers
#
# Uso:
#   python search.py index               → indicizza/aggiorna tutte le note
#   python search.py "query in italiano" → ricerca semantica
#   python search.py index "query"       → indicizza poi cerca subito

import chromadb
from sentence_transformers import SentenceTransformer
import os, glob, sys

KB_PATH = os.path.expanduser("~/Desktop/Magistrale/_KB")
DB_PATH = os.path.join(KB_PATH, ".chromadb")
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # ~120MB, capisce italiano

EXCLUDE = {"search.py", "_glossario.md"}


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection("kb")


def index():
    col = get_collection()
    model = SentenceTransformer(MODEL_NAME)
    files = [
        f for f in glob.glob(f"{KB_PATH}/**/*.md", recursive=True)
        if os.path.basename(f) not in EXCLUDE
    ]
    if not files:
        print("Nessun file .md trovato nella KB.")
        return

    added = 0
    for f in files:
        with open(f, encoding="utf-8") as fp:
            text = fp.read()
        # chunk da 500 char con overlap da 100
        chunks = [text[i:i+500] for i in range(0, len(text), 400)]
        ids = [f"{f}__{i}" for i in range(len(chunks))]
        embeddings = model.encode(chunks).tolist()
        metadatas = [{"file": f, "chunk": i} for i in range(len(chunks))]
        col.upsert(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
        added += len(chunks)

    print(f"Indicizzati {len(files)} file ({added} chunk totali).")


def search(query, n=5):
    col = get_collection()
    model = SentenceTransformer(MODEL_NAME)
    results = col.query(
        query_embeddings=model.encode([query]).tolist(),
        n_results=n
    )
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    print(f"\nRisultati per: \"{query}\"\n{'='*60}")
    seen_files = set()
    for doc, meta, dist in zip(docs, metas, distances):
        fpath = meta["file"]
        rel = os.path.relpath(fpath, KB_PATH)
        marker = " [NUOVO FILE]" if fpath not in seen_files else ""
        seen_files.add(fpath)
        score = round((1 - dist) * 100, 1)
        print(f"\n[{score}% rilevanza] {rel}{marker}")
        print(f"{doc[:300].strip()}...")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Uso:")
        print("  python search.py index               → indicizza la KB")
        print("  python search.py 'query'             → ricerca semantica")
        print("  python search.py index 'query'       → indicizza poi cerca")
        sys.exit(0)

    if args[0] == "index":
        index()
        if len(args) > 1:
            search(" ".join(args[1:]))
    else:
        search(" ".join(args))

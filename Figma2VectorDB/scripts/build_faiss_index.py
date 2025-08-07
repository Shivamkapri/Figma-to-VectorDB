#!/usr/bin/env python3
import json, pickle
import faiss
import numpy as np

EMBED_PATH = "data/embedded_nodes.json"
INDEX_PATH = "data/faiss.index"
META_PATH  = "data/faiss_meta.pkl"

def main():
    # Load embedded data
    with open(EMBED_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Stack embeddings into NumPy array
    embs = np.array([item["embedding"] for item in items], dtype="float32")
    ids  = [item["id"] for item in items]
    texts= [item["text"] for item in items]

    # Build FAISS index (Flat L2)
    dim = embs.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embs)

    # Persist index and metadata
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump({"ids": ids, "texts": texts}, f)

    print(f"✅ FAISS index built ({len(ids)} vectors) → {INDEX_PATH}")

def query_index(query: str, top_k: int = 5):
    # Load model & encoder
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load index & metadata
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)

    # Encode query
    q_emb = model.encode([query]).astype("float32")
    D, I = index.search(q_emb, top_k)

    print(f"\nSearch results for: “{query}”")
    for dist, idx in zip(D[0], I[0]):
        print(f"• {meta['ids'][idx]} [{dist:.4f}] → {meta['texts'][idx]}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        query_index(" ".join(sys.argv[2:]))
    else:
        main()

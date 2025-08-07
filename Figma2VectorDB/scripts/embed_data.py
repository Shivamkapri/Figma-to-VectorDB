#!/usr/bin/env python3
import json, sys
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"  # small & fast

def main():
    # Load nodes
    try:
        with open("data/text_nodes.json", "r", encoding="utf-8") as f:
            nodes = json.load(f)
    except Exception as e:
        print(f"❌ Error loading text_nodes.json: {e}", file=sys.stderr)
        sys.exit(1)

    # Load Sentence-Transformer model
    model = SentenceTransformer(MODEL_NAME)

    texts = [n["text"] for n in nodes]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Attach embeddings
    for node, emb in zip(nodes, embeddings):
        node["embedding"] = emb.tolist()

    # Save
    with open("data/embedded_nodes.json", "w", encoding="utf-8") as f:
        json.dump(nodes, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated embeddings for {len(nodes)} items → data/embedded_nodes.json")

if __name__ == "__main__":
    main()

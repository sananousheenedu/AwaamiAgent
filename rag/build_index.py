from pathlib import Path

from sentence_transformers import SentenceTransformer

from rag.embeddings import (
    MODEL_NAME,
    load_knowledge_base,
    generate_embeddings
)

from rag.vector_store import save_vector_store


KNOWLEDGE_PATH = Path(
    "knowledge_base/electricity/electricity_rules.json"
)

STORAGE_DIR = Path(
    "rag/storage/electricity"
)


def build_index():
    print("Loading knowledge base...")

    entries = load_knowledge_base(KNOWLEDGE_PATH)

    print(f"Knowledge entries: {len(entries)}")

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")

    embeddings = generate_embeddings(
        entries,
        model
    )

    print("Saving vector store...")

    save_vector_store(
        embeddings,
        entries,
        STORAGE_DIR
    )

    print("Index built successfully.")
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Storage: {STORAGE_DIR}")


if __name__ == "__main__":
    build_index()

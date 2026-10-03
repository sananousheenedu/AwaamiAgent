import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


def load_knowledge_base(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_search_text(entry):
    return " ".join([
        entry.get("topic", ""),
        entry.get("title", ""),
        entry.get("content", ""),
        entry.get("authority", ""),
        entry.get("source_name", "")
    ]).strip()


def generate_embeddings(entries, model):
    texts = [build_search_text(entry) for entry in entries]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":
    knowledge_path = Path(
        "knowledge_base/electricity/electricity_rules.json"
    )

    entries = load_knowledge_base(knowledge_path)

    model = SentenceTransformer(MODEL_NAME)

    embeddings = generate_embeddings(entries, model)

    print("Knowledge entries:", len(entries))
    print("Embeddings shape:", embeddings.shape)
    print("Embedding dimension:", embeddings.shape[1])

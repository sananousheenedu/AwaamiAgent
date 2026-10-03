import numpy as np
from sentence_transformers import SentenceTransformer

from rag.embeddings import MODEL_NAME
from rag.vector_store import load_vector_store


def retrieve(query, storage_dir, top_k=3):
    embeddings, entries = load_vector_store(storage_dir)

    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    scores = embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        entry = entries[index]

        results.append({
            "score": float(scores[index]),
            "id": entry.get("id", ""),
            "topic": entry.get("topic", ""),
            "title": entry.get("title", ""),
            "content": entry.get("content", ""),
            "authority": entry.get("authority", ""),
            "source_name": entry.get("source_name", ""),
            "source_url": entry.get("source_url", ""),
            "source_type": entry.get("source_type", ""),
            "verification_status": entry.get(
                "verification_status",
                ""
            )
        })

    return results

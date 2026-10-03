import json
from pathlib import Path
import numpy as np


def save_vector_store(embeddings, entries, storage_dir):
    storage_path = Path(storage_dir)
    storage_path.mkdir(parents=True, exist_ok=True)

    np.save(
        storage_path / "embeddings.npy",
        embeddings
    )

    with open(
        storage_path / "metadata.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            entries,
            file,
            ensure_ascii=False,
            indent=2
        )


def load_vector_store(storage_dir):
    storage_path = Path(storage_dir)

    embeddings = np.load(
        storage_path / "embeddings.npy"
    )

    with open(
        storage_path / "metadata.json",
        "r",
        encoding="utf-8"
    ) as file:
        entries = json.load(file)

    return embeddings, entries

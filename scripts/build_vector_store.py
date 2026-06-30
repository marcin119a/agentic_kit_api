"""
Eksportuje AIRLINE_FAQ do plików tekstowych (data/faq/*.txt) i buduje z nich
Vector Store w OpenAI API (do File Search / RAG).

Użycie:
    python -m scripts.build_vector_store
"""

import json
import random
from pathlib import Path

from openai import OpenAI

from app.faq.data import AIRLINE_FAQ
from config import Settings

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "faq"
VECTOR_STORE_NAME = "airline-faq_{}".format(random.random())
VECTOR_STORE_INFO_PATH = DATA_DIR / "vector_store.json"


def export_faq_to_txt() -> list[Path]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for category, text in AIRLINE_FAQ.items():
        path = DATA_DIR / f"{category}.txt"
        path.write_text(text.strip() + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def build_vector_store(client: OpenAI, paths: list[Path]) -> str:
    vector_store = client.vector_stores.create(name=VECTOR_STORE_NAME)

    file_streams = [path.open("rb") for path in paths]
    try:
        batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams,
        )
    finally:
        for stream in file_streams:
            stream.close()

    print(f"Status batcha uploadu: {batch.status}")
    print(f"Pliki: {batch.file_counts}")

    return vector_store.id


def main() -> None:
    settings = Settings()
    client = OpenAI(api_key=settings.openai_api_key)

    paths = export_faq_to_txt()
    print(f"Wyeksportowano {len(paths)} plików do {DATA_DIR}:")
    for path in paths:
        print(f"  - {path.name}")

    vector_store_id = build_vector_store(client, paths)
    print(f"\nVector store utworzony: {vector_store_id}")

    VECTOR_STORE_INFO_PATH.write_text(
        json.dumps({"name": VECTOR_STORE_NAME, "id": vector_store_id}, indent=2),
        encoding="utf-8",
    )
    print(f"Zapisano ID do {VECTOR_STORE_INFO_PATH}")


if __name__ == "__main__":
    main()
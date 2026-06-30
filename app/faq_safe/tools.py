import json
from pathlib import Path

from agents import function_tool
from openai import OpenAI

from app.faq.data import AIRLINE_FAQ
from config import Settings


VECTOR_STORE_INFO_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "faq" / "vector_store.json"
)

_client = OpenAI(api_key=Settings().openai_api_key)


@function_tool
def search_faq_vector_store(query: str) -> list[dict]:
    """
    Wyszukuje semantycznie najbardziej trafne fragmenty FAQ w Vector Store
    OpenAI (oparte na znaczeniu pytania, nie na dopasowaniu słów kluczowych
    jak search_airline_faq). Zwraca listę wyników: kategoria, ocena trafności
    (score) oraz treść fragmentu.
    """

    vector_store_id = json.loads(VECTOR_STORE_INFO_PATH.read_text(encoding="utf-8"))["id"]

    results = _client.vector_stores.search(
        vector_store_id=vector_store_id,
        query=query,
        max_num_results=3,
    )

    return [
        {
            "category": Path(result.filename).stem,
            "score": result.score,
            "content": "\n".join(part.text for part in result.content if part.type == "text"),
        }
        for result in results.data
    ]

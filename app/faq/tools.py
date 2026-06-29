from typing import Literal

from agents import function_tool

from app.faq.data import AIRLINE_FAQ

FAQCategory = Literal[
    "baggage",
    "check_in",
    "tickets",
    "refunds",
    "delays",
    "pets",
    "special_assistance"
]
@function_tool
def search_airline_faq(category: FAQCategory) -> dict:
    """
    Zwraca oficjalną treść FAQ dla podanej kategorii.
    Kategorię wybiera agent na podstawie własnego zrozumienia pytania pasażera,
    a nie na podstawie dopasowania słów kluczowych.
    """

    return {
        "category": category,
        "answer": AIRLINE_FAQ[category].strip(),
    }
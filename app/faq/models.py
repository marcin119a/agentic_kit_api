from typing import Literal

from pydantic import BaseModel


class FAQOutput(BaseModel):
    category: Literal[
        "baggage",
        "check_in",
        "tickets",
        "refunds",
        "delays",
        "pets",
        "special_assistance",
        "other",
    ]
    answer: str
    confidence: float
    needs_human_support: bool
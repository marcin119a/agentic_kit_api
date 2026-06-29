
from pydantic import BaseModel
from typing import Literal

class EscalationOutput(BaseModel):
    category: Literal[
        "complaint",
        "compensation",
        "payment",
        "personal_data",
        "legal",
        "other",
    ]
    summary: str
    priority: Literal["low", "medium", "high"]
    requires_human_contact: bool
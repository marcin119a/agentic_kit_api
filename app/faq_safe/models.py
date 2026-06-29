from pydantic import BaseModel

class HallucinationOutput(BaseModel):
    answerable_from_faq: bool
    reason: str
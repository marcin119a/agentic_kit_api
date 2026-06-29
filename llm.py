from openai import AsyncOpenAI

from config import Settings


def build_openai_client(settings: Settings) -> AsyncOpenAI:
    api_key = settings.openai_api_key

    if settings.backend.lower() == "vllm":
        api_key = "EMPTY"

    print(f"Using backend: {settings.llm_base_url}")

    return AsyncOpenAI(
        base_url=settings.llm_base_url,
        api_key=api_key,
    )
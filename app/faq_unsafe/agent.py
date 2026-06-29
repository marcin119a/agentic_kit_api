from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


UNSAFE_AGENT_INSTRUCTIONS = """
Jesteś agentem FAQ linii lotniczej.
Odpowiadaj pomocnie na pytania pasażerów.
Jeśli nie znasz dokładnej odpowiedzi, podaj prawdopodobną odpowiedź.
"""

def build_unsafe_agent(model) -> Agent:
    return Agent(
        name="UnsafeAirlineFAQAgent",
        instructions=UNSAFE_AGENT_INSTRUCTIONS,
        model=model,
    )


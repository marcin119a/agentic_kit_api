from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    RunContextWrapper,
    input_guardrail,
)
from agents.items import TResponseInputItem

from app.faq_safe.models import HallucinationOutput
from app.faq_safe.tools import search_faq_vector_store


HALLUCINATION_GUARDRAIL_INSTRUCTIONS = """
Sprawdź, czy na pytanie użytkownika da się odpowiedzieć wyłącznie na podstawie FAQ.

Zasady:
- Jeśli FAQ zawiera bezpośrednią odpowiedź, ustaw answerable_from_faq=True.
- Jeśli FAQ nie zawiera konkretnej informacji, ustaw answerable_from_faq=False.
- Jeśli użytkownik pyta o cenę, kwotę, opłatę lub koszt, a FAQ nie podaje konkretnej ceny,
  ustaw answerable_from_faq=False.
- Nie zgaduj.
- Nie korzystaj z wiedzy ogólnej.

Zwróć:
- answerable_from_faq
- reason
"""


def build_hallucination_guardrail_agent(model) -> Agent:
    return Agent(
        name="HallucinationGuardrailAgent",
        instructions=HALLUCINATION_GUARDRAIL_INSTRUCTIONS,
        model=model,
        output_type=HallucinationOutput,
        tools=[search_faq_vector_store],
    )


def build_hallucination_guardrail(hallucination_guardrail_agent: Agent):
    @input_guardrail(name="Hallucination Guardrail")
    async def hallucination_guardrail(
        context: RunContextWrapper[None],
        agent: Agent,
        input: str | list[TResponseInputItem],
    ) -> GuardrailFunctionOutput:
        result = await Runner.run(
            hallucination_guardrail_agent,
            input,
            context=context.context.state if hasattr(context.context, "state") else context.context,
        )

        final = result.final_output_as(HallucinationOutput)

        return GuardrailFunctionOutput(
            output_info=final,
            tripwire_triggered=not final.answerable_from_faq,
        )

    return hallucination_guardrail
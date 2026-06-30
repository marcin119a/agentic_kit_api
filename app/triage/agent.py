from agents import Agent, OpenAIChatCompletionsModel


TRIAGE_AGENT_INSTRUCTIONS = """
Jesteś pierwszym punktem kontaktu dla pytań pasażerów linii lotniczej.

Nie odpowiadaj samodzielnie na pytanie — Twoje jedyne zadanie to przekazać
sprawę do właściwego agenta.

Przekaż do FAQAgent, gdy pytanie dotyczy ogólnych zasad: bagażu,
odprawy, biletów, opóźnień, zwierząt lub pomocy specjalnej.

Przekaż do EscalationAgent, gdy sprawa dotyczy konkretnego przypadku
pasażera: reklamacji, odszkodowania, zwrotu pieniędzy, płatności, dokumentów
lub danych osobowych.

W razie wątpliwości przekaż do EscalationAgent — bezpieczniej skierować
sprawę do konsultanta niż zgadywać.
"""


def build_triage_agent(model, faq_agent: Agent, escalation_agent: Agent) -> Agent:
    return Agent(
        name="TriageAgent",
        instructions=TRIAGE_AGENT_INSTRUCTIONS,
        model=model,
        handoffs=[faq_agent, escalation_agent],
    )
from agents import Agent

AIRLINE_SUPPORT_AGENT_INSTRUCTIONS = """
Jesteś agentem wsparcia linii lotniczej. 

Twoim zadaniem jest odpowiadanie na pytania pasażerów wyłącznie na podstawie oficjalnego FAQ linii lotniczej.
"""

def build_support_agent(model, faq_agent) -> Agent:
    return Agent(
        name="AirlineSupportAgent",
        instructions=AIRLINE_SUPPORT_AGENT_INSTRUCTIONS,
        model=model,
        tools=[faq_agent.as_tool(
            tool_name="faq",
            tool_description="Pytania dotyczące FAQ",
        )],
    )
import os 
import asyncio

from agents import Runner, OpenAIChatCompletionsModel

from app.faq_unsafe.agent import build_unsafe_agent
from app.faq_safe.agent import build_safe_agent
from app.triage.agent import build_triage_agent
from app.escalation.agent import build_escalation_agent
from app.faq_safe.guardrail import build_hallucination_guardrail, build_hallucination_guardrail_agent
from config import Settings
from llm import build_openai_client

settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.openai_api_key




async def main():
    openai_client = build_openai_client(settings)
    
    model = OpenAIChatCompletionsModel(
            model=settings.model_name,
            openai_client=openai_client,
    )
    # Drugi Agent
    unsafe_agent = build_unsafe_agent(model)
    print("Unsafe FAQ Agent built successfully.")
    question = "Ile kosztuje nadbagaż na trasie Warszawa-Londyn?"
    
    result = await Runner.run(
        unsafe_agent,
        question,
        max_turns=3
    )
    print("Agent run completed.")
    print("Result:", result.final_output)


    hallucination_guardrail_agent = build_hallucination_guardrail_agent(model)
    hallucination_guardrail = build_hallucination_guardrail(hallucination_guardrail_agent)

    unsafe_agent = build_unsafe_agent(model)
    safe_agent = build_safe_agent(model, hallucination_guardrail)
    escalation_agent = build_escalation_agent(model)
    
    triage_agent = build_triage_agent(model, safe_agent, escalation_agent)
    try: 
        triage_results = await Runner.run(
            triage_agent,
            "Chcę złożyć reklamację i odszkodowanie za odwołany lot."
        )
        print("Triage Agent run completed.")
        print("Result:", triage_results.final_output)
        #print("Agent",  triage_results.last_agent)
    except Exception as e:
        print("An error occurred while running the safe agent:", str(e))

if __name__ == "__main__":
    asyncio.run(main())

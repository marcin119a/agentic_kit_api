from datetime import datetime
import os 
import asyncio

from agents import Runner, OpenAIChatCompletionsModel

from app.faq_unsafe.agent import build_unsafe_agent
from app.faq_safe.agent import build_safe_agent
from app.triage.agent import build_triage_agent
from app.escalation.agent import build_escalation_agent
from app.faq_safe.guardrail import build_hallucination_guardrail, build_hallucination_guardrail_agent
from app.memory import PassengerSQLiteSession
from config import Settings
from llm import build_openai_client

settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.openai_api_key




async def main():
    session = PassengerSQLiteSession(f"unsafe_demo{datetime.now()}", passenger_id="demo_passenger", db_path="session.db")
    await session.remember_fact("Pasażer jest kobietą")

    openai_client = build_openai_client(settings)
    
    model = OpenAIChatCompletionsModel(
            model=settings.model_name,
            openai_client=openai_client,
    )

    hallucination_guardrail_agent = build_hallucination_guardrail_agent(model)
    hallucination_guardrail = build_hallucination_guardrail(hallucination_guardrail_agent)

    safe_agent = build_safe_agent(model, hallucination_guardrail)
    escalation_agent = build_escalation_agent(model)
    
    triage_agent = build_triage_agent(model, safe_agent, escalation_agent)
    try: 
        triage_results = await Runner.run(
            triage_agent,
            "Chcę złożyć reklamację",
            session=session
        )
        print("Triage Agent run completed.")
        print("Result:", triage_results.final_output)

        ones_again = await Runner.run(
            triage_agent,
            "Chodzi mi o odszkodowanie za odwołany lot.",
            session=session
        )
        print("Triage Agent run completed.")
        print("Result:", ones_again.final_output)

        #print("Agent",  triage_results.last_agent)
    except Exception as e:
        print("An error occurred while running the safe agent:", str(e))

if __name__ == "__main__":
    asyncio.run(main())

import os 
import asyncio

from agents import Runner, OpenAIChatCompletionsModel

from app.faq_unsafe.agent import build_unsafe_agent
from app.faq_safe.agent import build_safe_agent
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
        question
    )
    print("Agent run completed.")
    print("Result:", result.final_output)


    hallucination_guardrail_agent = build_hallucination_guardrail_agent(model)
    hallucination_guardrail = build_hallucination_guardrail(hallucination_guardrail_agent)

    unsafe_agent = build_unsafe_agent(model)
    safe_agent = build_safe_agent(model, hallucination_guardrail)
    
    try: 
        print("Safe FAQ Agent built successfully.")
        question = "Ile kosztuje nadbagaż na trasie Warszawa-Londyn?"
        
        result = await Runner.run(
            safe_agent,
            question
        )
        print("Agent run completed.")
        print("Result:", result.final_output)
    except Exception as e:
        print("An error occurred while running the safe agent:", str(e))

if __name__ == "__main__":
    asyncio.run(main())

import os 
import asyncio

from agents import Runner

from app.faq.agent import build_faq_agent
from config import Settings
from llm import build_openai_client

settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.openai_api_key



async def main():
    openai_client = build_openai_client(settings)


    agent = build_faq_agent(openai_client, settings)
    question = "Czy mogę zabrać psa?"

    try:
       print("\n--- DEMO 1: Agent bez guardraila ---")
       unsafe_result = await Runner.run(
           agent,
           question,
       )
       print(unsafe_result.final_output)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

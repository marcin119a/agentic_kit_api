from datetime import datetime
import os 
import asyncio

from agents import Runner, OpenAIChatCompletionsModel

from app.faq.agent import build_faq_agent
from config import Settings
from llm import build_openai_client

settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.openai_api_key




async def main():
    openai_client = build_openai_client(settings)
    faq_agent, mcp_helper_server = build_faq_agent(openai_client, settings)
    async with mcp_helper_server:
        result = await Runner.run(
            faq_agent,
            "(2+3)*5",
            max_turns=3
        )
        print("FAQ Agent run completed.")
        print("Result:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
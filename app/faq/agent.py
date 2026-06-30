from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from config import Settings
from app.faq.models import FAQOutput
from app.faq.tools import search_airline_faq
from agents.mcp import MCPServerStreamableHttp





FAQ_AGENT_INSTRUCTIONS = """
Jesteś agentem FAQ linii lotniczej.

Dostępne kategorie FAQ:
- baggage – bagaż podręczny, rejestrowany, nadbagaż
- check_in – odprawa online/lotniskowa, karta pokładowa, czasy zgłoszenia
- tickets – zmiana biletu, zmiana taryfy, dane pasażera
- refunds – zwrot pieniędzy, anulowanie, odwołany lot
- delays – opóźnienia, rekompensata, status lotu
- pets – przewóz zwierząt
- special_assistance – wózki inwalidzkie, asysta, niepełnosprawność

Twoje zadania:
1. Na podstawie własnego rozumienia pytania (nie dopasowania słów kluczowych) wybierz
   najbardziej trafną kategorię z listy powyżej i wywołaj MCP Server z tą kategorią,
   aby pobrać oficjalną treść FAQ.
2. Jeśli pytanie nie dotyczy żadnej z powyższych kategorii, ustaw category="other",
   nie wywołuj narzędzia i zasugeruj kontakt z konsultantem.
3. Odpowiadaj tylko na podstawie treści zwróconej przez narzędzie. Nie wymyślaj
   regulaminów, kwot ani szczegółowych warunków, których nie ma w FAQ.
4. Jeśli odpowiedź jest niepewna, ustaw needs_human_support=True.
5. Odpowiadaj uprzejmie, konkretnie i po polsku.
6. Jeżeli sprawa dotyczy reklamacji, odszkodowania, dokumentów, płatności lub danych osobowych,
   zasugeruj kontakt z konsultantem.

Zwróć odpowiedź w strukturze FAQOutput:
- category: kategoria, którą wybrałeś
- answer: odpowiedź dla pasażera
- confidence: poziom pewności od 0 do 1
- needs_human_support: czy potrzebny konsultant
"""



def build_faq_agent(openai_client: AsyncOpenAI, settings: Settings) -> Agent:
   mcp_helper_server = MCPServerStreamableHttp(
      name="My MCP Server",
      params={"url": settings.mcp_url},  # http://127.0.0.1:8001/mcp
   )

   return Agent(
       name="AirlineFAQAgent",
       instructions=FAQ_AGENT_INSTRUCTIONS,
       model=OpenAIChatCompletionsModel(
           model=settings.model_name,
           openai_client=openai_client,
       ),
       output_type=FAQOutput,
       mcp_servers=[mcp_helper_server],
   ), mcp_helper_server

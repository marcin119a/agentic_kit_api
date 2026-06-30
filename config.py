from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   model_config = SettingsConfigDict(env_file=".env", extra="ignore")

   backend: str = "openai"
   llm_base_url: str = "https://api.openai.com/v1"
   model_name: str = "gpt-4o-mini"
   openai_api_key: str
   mcp_url: str = "http://127.0.0.1:8001/mcp"

from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from agents.run import RunConfig
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
external_provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)
model = OpenAIChatCompletionsModel(
    openai_client=external_provider,
    model="gemini-2.0-flash",
)

config = RunConfig(
    model=model, 
    model_provider=external_provider, 
    # tracing_disabled=True
    )

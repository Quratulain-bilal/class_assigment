from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, enable_verbose_stdout_logging, RunConfig
from dotenv import load_dotenv
from rich import print
import os


set_tracing_disabled(disabled=True)
load_dotenv()
enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

english_agent = Agent(
    name="English Linguistic",
    instructions="You are expert in English language",
    model=model
)

spanish_agent = Agent(
    name="Spanish Linguistic",
    instructions="You are expert in Spanish language",  # 
    model=model
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate. "
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        english_agent.as_tool(
            tool_name="translate_to_english",
            tool_description="Translate the user's message to English"
        ),
        spanish_agent.as_tool( 
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        )
    ],
    model=model
)

result = Runner.run_sync(
    starting_agent=orchestrator_agent,
    input="'tum kia kar rahy ho', translate it to english and mera name annie hai ,translate this to spanish"
)

print(result.final_output)

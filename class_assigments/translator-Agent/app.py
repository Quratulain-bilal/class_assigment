from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner,RunConfig
import os
import asyncio
import chainlit as cl

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = 'gemini-2.0-flash'

# External client
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model setup
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

# Define agents
joke_agent = Agent(
    name="comedian",
    instructions="create funny jokes on any topic",
    model=model
)



friendly_agent = Agent(
    name="Translator_Agent",
    instructions="You're a kind and translator agent of any language  "
                 "Make the user feel like they’re chatting with a friend. Use emojis sometimes.",
    model=model
)

# Disable tracing
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Handle user messages
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.lower()

    # Step 1: Initialize memory (if not already)
    if cl.user_session.get("memory") is None:
        cl.user_session.set("memory", [])

    memory = cl.user_session.get("memory")

    # Show typing animation
    chat_msg = await cl.Message(content="Thinking...", author="Assistant").send()
    await asyncio.sleep(0.5)



    context = "\n".join(memory)
    combined_input = context + f'\nuser {user_input}'
    

    # Run the selected agent
    result = await Runner.run(friendly_agent, combined_input, run_config=config)

    # Show result in Chainlit
    # await cl.Message(content=f"{label}:\n{result.final_output}").send()

    memory.append(f"user: {user_input}")
    memory.append(f"assistant: {result.final_output}")
    cl.user_session.set("memory", memory)


    # Add label (agent name)
    label = friendly_agent.name
    full_response = f"{label}:\n{result.final_output}"

    displayed = ""
    for char in full_response:
        displayed += char
        chat_msg.content = displayed
        await chat_msg.update()
        await asyncio.sleep(0.06)  # Adjust typing speed here

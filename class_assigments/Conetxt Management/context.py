import asyncio
from agents import Agent , RunContextWrapper, function_tool,Runner
from connection import config
from rich import print
from pydantic import BaseModel

class UserInfo(BaseModel):
    name:str
    age:int
@function_tool
def context_provider(ctx:RunContextWrapper[UserInfo]):
    return f"User info: {ctx.context.name},{ctx.context.age}"

animal_agent = Agent(
    name="Animal Agent",
    instructions="""
    You are a helpful assistant that can help with animal related questions.
    Greet the user first with his name,
    For example: "Hello Sarah, how can I help you today?"
    You will be given a user request and you will need to determine if it is a animal related question.
    If it is, you will need to provide the user with the information they are looking for.
    If it is not, You will politely decline to answer the question.
    """,
    tools=[context_provider]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
   You are a helpful assistant who always transfer the user query to the animal agent.
    """,
    handoffs=[animal_agent],
    tools=[context_provider]
)

async def main():
    user_info = UserInfo(name="Sarah", age=25)
    runner = await  Runner.run(
                    triage_agent,
                    "Hello",
                    run_config=config,
                    context=user_info
                    )
    print(runner.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())







import asyncio
from typing import Dict
from agents import Agent , Runner, function_tool, RunContextWrapper, enable_verbose_stdout_logging
from connection import config
from pydantic import BaseModel
from rich import print
# enable_verbose_stdout_logging()


class UserInfo(BaseModel):
    name:str
    age:int
    address:Dict[str,str]
class ContextOutput(BaseModel):
    user_info:UserInfo
@function_tool
def context(ctx:RunContextWrapper[UserInfo])->str:
    # return f"User info: {ctx.context.name},{ctx.context.age},{ctx.context.address}"
    # print(f"Context: {ctx.context.model_dump_json()}")
    # return ContextOutput(user_info=ctx.context)
    return f"User info: {ctx.context.name},{ctx.context.age},{ctx.context.address['city']},{ctx.context.address['state']},{ctx.context.address['country']}"

animal_agent = Agent(
    name="Animal Agent",
    instructions="""
    You are a helpful assistant that can help with animal related questions.
    Greet the user first with his name,
    For example: "Hello Sarah, how can I help you today?"
    You will be given a user request and you will need to determine if it is a animal related question.
    If it is, you will need to provide the user with the information they are looking for.
    If it is not, You will respectfully decline to answer the question.
    """,
    tools=[context]

)
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a helpful assistant who help to transfer the user query to the appropriate sub-agent.
    """,
    tools=[context],
    handoffs=[animal_agent]
    
)


async def main():
    user_info = UserInfo(
        name="Sarah",
        age=25,
        address={"city":"New York", "state":"NY", "country":"USA"}
    )
    result = await Runner.run(triage_agent, "How loud does a dog barks?",run_config=config,context=user_info)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

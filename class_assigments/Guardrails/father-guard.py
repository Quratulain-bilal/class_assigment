import asyncio
from agents import Agent,Runner,  input_guardrail, GuardrailFunctionOutput,RunContextWrapper,TResponseInputItem, InputGuardrailTripwireTriggered, trace
from pydantic import BaseModel
from connection import config
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Exercise # 2 Objective: Make a father agent and father guardrail. The father stopping his child to run below 26C.


class FatherOutput(BaseModel):
    user_input:str
    response:str
    is_temperature_below_26C:bool
    
father_guardrail_agent = Agent(
    name="Father Guardrail Agent",
    instructions="Your task is to check if the user query is related to AC temperature or not. if it is then check if the temperature is below 26C or not",
    output_type=FatherOutput
)
# input guardrail trigger function
@input_guardrail
async def father_guard(ctx:RunContextWrapper, agent:Agent, input:TResponseInputItem):
    print(input)
    result = await Runner.run(father_guardrail_agent, input, run_config=config)
    # triggeredValue = True if "slot change" in result.final_output else False
    # print(triggeredValue)
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered = result.final_output.is_temperature_below_26C
    )
    
son_agent = Agent(
    name="Son Agent",
    instructions="You are a Son agent",
    input_guardrails=[father_guard]
)

async def main():
    try:
        with trace("Father Agent"):
            result = await Runner.run(son_agent, "The AC is on 18C", run_config=config)
            print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("You can not run below 26C")
    
    
asyncio.run(main())

# Test Input: "The AC is on 18C." (Tripwire Triggered)
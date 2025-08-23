import asyncio
from agents import Agent,Runner,  input_guardrail, GuardrailFunctionOutput,RunContextWrapper,TResponseInputItem, InputGuardrailTripwireTriggered, trace
from pydantic import BaseModel
from connection import config
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Exercise # 3 Objective: Make a gate keeper agent and gate keeper guardrail. The gate keeper stopping students of other school.

class GateKeeperOutput(BaseModel):
    user_input:str
    response:str
    isStudentOfOtherSchool:bool
    
gate_keeper_guardrail_agent = Agent(
    name="Gate Keeper Guardrail Agent",
    instructions="Your school name is Naimal's Darsgah. Your task is to check if the user query is related to student of other school entering in your school or not.",
    output_type=GateKeeperOutput
)
# input guardrail trigger function
@input_guardrail
async def gate_keeper_guard(ctx:RunContextWrapper, agent:Agent, input:TResponseInputItem):
    
    result = await Runner.run(gate_keeper_guardrail_agent, input, run_config=config)
    # triggeredValue = True if "slot change" in result.final_output else False
    # print(triggeredValue)
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered = result.final_output.isStudentOfOtherSchool
    )
    
student_agent = Agent(
    name="Student Agent",
    instructions="You are a student agent",
    input_guardrails=[gate_keeper_guard]
)

async def main():
    try:
        with trace("Gate Keeper Agent"):
            result = await Runner.run(student_agent, "Hey i am Sarah from Naimal's Darsgah", run_config=config)
            print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("You are not allowed to enter in Naimal's Darsgah")
    
    
asyncio.run(main())

# Test Input: "Hey I am Sarah from Hiast College." (Tripwire Triggered)
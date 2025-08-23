import asyncio
from agents import Agent,Runner,  input_guardrail, GuardrailFunctionOutput,RunContextWrapper,TResponseInputItem, InputGuardrailTripwireTriggered, trace
from pydantic import BaseModel
from connection import config
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Exercise # 1 Objective: Make a agent and make an input guardrail trigger. Prompt: I want to change my class timings 😭😭 Outcome: After running the above prompt an InputGuardRailTripwireTriggered in except should be called. See the outcome in LOGS


class TeacherOutput(BaseModel):
    user_input:str
    response:str
    isSlotChnage:bool
    
teacher_guardrail_agent = Agent(
    name="Teacher Guardrail Agent",
    instructions="Your task is to check if the user query is related to slot/ time/ class change or not.",
    output_type=TeacherOutput
)
# input guardrail trigger function
@input_guardrail
async def teacher_guard(ctx:RunContextWrapper, agent:Agent, input:TResponseInputItem):
    result = await Runner.run(teacher_guardrail_agent, input, run_config=config)
    # triggeredValue = True if "slot change" in result.final_output else False
    # print(triggeredValue)
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered = result.final_output.isSlotChnage
    )
    
student_agent = Agent(
    name="Student Agent",
    instructions="You are a student agent",
    input_guardrails=[teacher_guard]
)

async def main():
    try:
        with trace("Teacher Agent"):
            result = await Runner.run(student_agent, "I want to change make pizza", run_config=config)
            print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("This is not allowed")
    
    
asyncio.run(main())
# Test Input: "I want to change my slot from thursday morning to sunday afternoon." (Tripwire Triggered)
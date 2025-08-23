import asyncio
from agents import Agent,Runner,  input_guardrail, GuardrailFunctionOutput,RunContextWrapper,TResponseInputItem, InputGuardrailTripwireTriggered, trace
from pydantic import BaseModel
from connection import config
from dotenv import load_dotenv
from rich import print
load_dotenv()

# Exercise # 1 Objective: Make a agent and make an input guardrail trigger. Prompt: I want to change my class timings 😭😭 Outcome: After running the above prompt an InputGuardRailTripwireTriggered in except should be called. See the outcome in LOGS
class EmailGuardrailOutput(BaseModel):
    email_body:str
    isEmailValid:bool

email_Guardrail_agent = Agent(
    name="Email Guardrail Agent",
    instructions="""You are an email guardrail agent.
    You will check if the user input is in the provided format or not.
    """,
    output_type=EmailGuardrailOutput
)

@input_guardrail
async def email_guard(ctx:RunContextWrapper, agent:Agent, input:TResponseInputItem):
    result = await Runner.run(email_Guardrail_agent, input, run_config=config)
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered = result.final_output.isSlotChnage
    )

email_agent = Agent(
    name="Email Agent", 
    instructions="""You are an email agent.
    You will be provided with the email body and the user email address.
    You will need to send the email to the user with the email body.
    """,
    input_guardrails=[email_guard]

)


class TeacherOutput(BaseModel):
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
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered = result.final_output.isSlotChnage
    )
    
student_agent = Agent(
    name="Student Agent",
    instructions="You are a student agent, you will be provided with the user query and you will need to check if the user query is related to slot/ time/ class change or not. If it is, you will need to call the teacher guardrail agent. If it is not, you will need to call the email agent.",
    input_guardrails=[teacher_guard],
    handoffs=[email_agent]
    
)

async def main():
    try:
        with trace("Teacher Agent"):
            result = await Runner.run(student_agent, "Write an email to Sara to inform her about the test on Monday.", run_config=config)
            print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Invalid query")
    
    
asyncio.run(main())
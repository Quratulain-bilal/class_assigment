import asyncio
from agents import Agent, RunContextWrapper, function_tool,Runner
from connection import config
from rich import print
from pydantic import BaseModel

class StudentProfile(BaseModel):
    student_id:str
    student_name:str
    current_semester:int
    total_courses:int

@function_tool
def get_std_profile_info(ctx:RunContextWrapper[StudentProfile]):
    return f"Student ID: {ctx.context.student_id}, Student Name: {ctx.context.student_name}, Current Semester: {ctx.context.current_semester}, Total Courses: {ctx.context.total_courses}"

std_agent = Agent(
    name="Student Profile Agent",
    instructions="You are an student profile agent that uses the get_std_profile_info tool to get the student profile information",
    tools=[get_std_profile_info],
    
)

async def main():
  

    student = StudentProfile(
        student_id="STU-456",
        student_name="Hassan Ahmed",
        current_semester=4,
        total_courses=5
    )

    result = await Runner.run(std_agent, "What kind of question you may answer", run_config=config, context=student)
    print(result.final_output)
asyncio.run(main())
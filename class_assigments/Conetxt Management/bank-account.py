import asyncio
from agents import Agent, RunContextWrapper, function_tool,Runner
from connection import config
from rich import print
from pydantic import BaseModel

class BankAccount(BaseModel):
    account_number:str
    customer_name:str
    account_balance:float
    account_type:str

@function_tool
def get_bank_account_info(ctx:RunContextWrapper[BankAccount]):
    return f"Account number: {ctx.context.account_number}, Customer name: {ctx.context.customer_name}, Account balance: {ctx.context.account_balance}, Account type: {ctx.context.account_type}"

acc_agent = Agent(
    name="Account Agent",
    instructions="You are an account agent that can get the bank account information",
    tools=[get_bank_account_info],
    
)

async def main():
    bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500.50,
    account_type="savings"
)
    result = await Runner.run(acc_agent, "Give me my bank details", run_config=config, context=bank_account)
    print(result.final_output)
asyncio.run(main())
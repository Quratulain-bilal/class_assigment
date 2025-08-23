from shopping_agent import shopping_agent
from connection import config
from agents import Runner
from rich import print

#Use these inputs to test the agent
# input = "How many brands are there in your store?"
# input="Show me Al-Ekhtiari collection of your store."
# input="Show me male collection of your store"
# input="Show me female collection of your store"
# input="Show me unisex collection of your store"
# input="What's in your store?"


runner = Runner.run_sync(starting_agent=shopping_agent, input="What's in your store?", run_config=config)
print(runner.final_output)
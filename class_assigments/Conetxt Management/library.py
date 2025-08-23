import asyncio
from agents import Agent, RunContextWrapper, function_tool,Runner
from connection import config
from rich import print
from pydantic import BaseModel

class LibraryBook(BaseModel):
    book_id:str
    book_title:str
    author_name:str
    is_available:bool

@function_tool
def get_library_info(ctx:RunContextWrapper[LibraryBook]):
    return f"Author name: {ctx.context.author_name}, Book title: {ctx.context.book_title}, Book ID: {ctx.context.book_id}, Is Available: {ctx.context.is_available}"

library_agent = Agent(
    name="Library Agent",
    instructions="You are a Library agent that can get the book details from get_library_info tool.",
    tools=[get_library_info],
    
)

async def main():
   # 3. LIBRARY BOOK CONTEXT
    library_book = LibraryBook(
        book_id="BOOK-123",
        book_title="Python Programming",
        author_name="John Smith",
        is_available=True
    )
    result = await Runner.run(library_agent, "Give me book details", run_config=config, context=library_book)
    print(result.final_output)
asyncio.run(main())


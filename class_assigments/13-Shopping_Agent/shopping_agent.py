from agents import Agent

from tool import brand_count, category_count, fetch_brand_specific_data, fetch_gender_specific_data, fetch_shopping_data

shopping_agent = Agent(
    name="Shopping Agent",
    instructions="""You are a shopping agent which response the user from the provided tools.
    If you got anything like a list of brands, or list or categories then make a list display for list items.
    If you got any number then make a number display for the number.
    If you got any error then make a error display for the error.
    if you got any other thing then make a text display for the thing.
    If you got the whole data then make a table display for the data.""",
    tools=[fetch_shopping_data,fetch_gender_specific_data,category_count, brand_count,fetch_brand_specific_data]
)
from agents import function_tool
import requests
import os
from dotenv import load_dotenv
load_dotenv()
url=os.getenv("SHOPPING_API_URL")

@function_tool
def fetch_shopping_data():
    print("fetch shopping data function called")
    response =  requests.get(url)
    return response.json()

@function_tool
def fetch_gender_specific_data(gender:str):
    print("gender specific data function called")
    gender=gender.title()
    response = requests.get(url)
    if response.status_code == 200:
        response_data=response.json()
        filtered_data = [item for item in response_data if item["gender"]==gender]
        if filtered_data:
            return filtered_data
        else:
            return f"Error: No data found for {gender}"
    else:
        return f"Error: Invalid gender"
    
@function_tool
def fetch_brand_specific_data(brand:str):
    print("brand specific data function called")
    response = requests.get(url)
    if response.status_code == 200:
        response_data=response.json()
        filtered_data = [item for item in response_data if item["brand"].lower()==brand.lower()]
        if filtered_data:
            return filtered_data
        else:
            return f"Error: No data found for {brand}"
    else:
        return f"Error: Invalid brand"
    
@function_tool
def brand_count():
    print("brand count function called")
    response = requests.get(url)
    if response.status_code == 200:
        response_data=response.json()
        brands = set(item["brand"] for item in response_data)
        return f"We have {len(brands)} different brands in our store, '{', '.join(brands)}'"
    else:
        return f"Error: Failed to fetch brands"

@function_tool	
def category_count():
    print("category count function called")
    return f"We have 2 categories in our store, 'Watches' and 'Perfume'"

#  python -m uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import random

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Load quotes data from the file
with open("quotes.json", "r") as file:
    quotes_data = json.load(file)

# API endpoint to get all quotes
@app.get("/quotes")
def get_all_quotes():
    return JSONResponse(content=quotes_data)

@app.get("/quotes/random")
def get_random_quote():
    random_quote = random.choice(quotes_data)
    return JSONResponse(content=random_quote)

@app.get("/quotes/author/{author}")
def get_quotes_by_author(author: str):
    quotes = [quote for quote in quotes_data if quote["author"] == author]
    return JSONResponse(content=quotes)

@app.get('/quotes/category/{category}')
def get_quotes_by_category(category: str):
    filterQuote = [quote for quote in quotes_data if quote.get("category", "").lower() == category.lower()]
    if not filterQuote:
        return JSONResponse(content={"error": f"No quotes found for the category: {category}"})
    return JSONResponse(content=filterQuote)
    

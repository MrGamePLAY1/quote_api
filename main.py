#  python -m uvicorn main:app --reload
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json
import random

app = FastAPI()

# Model for the quote
class Quote(BaseModel):
    id: int
    author: str
    quote: str
    category: str


# Placeholder data store (in-memory list for demonstration purposes)
quotes_data = []


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
    if not quotes:
        return JSONResponse(content={"error": f"No quotes found for the category: {author}"})
    return JSONResponse(content=quotes)

@app.get('/quotes/category/{category}')
def get_quotes_by_category(category: str):
    filterQuote = [quote for quote in quotes_data if quote.get("category", "").lower() == category.lower()]
    if not filterQuote:
        return JSONResponse(content={"error": f"No quotes found for the category: {category}"})
    return JSONResponse(content=filterQuote)
    
@app.get('/quotes/randomAuthor')
def get_random_author():
    random_author = random.choice(quotes_data)
    if not random_author:
        return JSONResponse(content={"error": f"No quotes found for the category: {author}"})
    return JSONResponse(content=random_author)

# List of authors in the quotes data
@app.get("/authors")
def get_authors():
    author = [quote["author"] for quote in quotes_data]
    return JSONResponse(content=author)

# List of categories in the quotes data
@app.get("/categories")
def get_catgories():
    new_list = []
    for quote in quotes_data:
        if quote["category"] not in new_list:
            new_list.append(quote["category"])
    return JSONResponse(content=new_list)



# Adding new quote
@app.post("/quotes/add")
async def add_quote(quote: Quote):
    new_quote = {
        "id": len(quotes_data) + 1,  # Generate a unique ID for the quote
        "quote": quote.quote,
        "author": quote.author,
        "category": quote.category
    }
    quotes_data.append(new_quote)
    return {"message": "Quote added successfully", "quote": new_quote}
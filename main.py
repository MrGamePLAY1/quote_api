# Windows: #  python -m uvicorn main:app --reload 
# Mac: #  python3 -m uvicorn main:app --reload 
# pip install fastapi



# macOS python3 -m pip install xxxx

from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json
import os
import random

role_permission: dict[str, list[str]] = {
    'admin': ['read', 'write', 'update', 'delete'],
    'editor': ['read', 'write', 'update'],
    'viewer': ['read']
}

users = dict[str, dict[str, list[str]]] = {
    'user1': {'roles': ['admin']},
    'user2': {'roles': ['editor']},
    'user3': {'roles': ['viewer']}
}

app = FastAPI()

# Placeholder data store (in-memory list for demonstration purposes)
quotes_data = []

# Get current user
def get_current_user(request: Request):
    user = request.headers.get('username')
    if not user or user not in users:
        raise HTTPException(status_code=401, detail="Unauthorised")
    return users[user]


#--------------Default root-------------------


@app.get("/")
def read_root():
    return {"Hello": "World"}

#---------------------------------------------


# Load quotes data from the file
with open("quotes.json", "r") as file:
    quotes_data = json.load(file)

# API endpoint to get all quotes
@app.get("/quotes")
def get_all_quotes():
    return JSONResponse(content=quotes_data)

# /quotes/random
@app.get("/quotes/random")
def get_random_quote():
    random_quote = random.choice(quotes_data)
    return JSONResponse(content=random_quote)

# /quotes/author/Bill Gates
@app.get("/quotes/author/{author}")
def get_quotes_by_author(author: str):
    quotes = [quote for quote in quotes_data if quote["author"] == author]
    if not quotes:
        return JSONResponse(content={"error": f"No quotes found for the category: {author}"})
    return JSONResponse(content=quotes)

# /quotes/category/Technology
@app.get('/quotes/category/{category}')
def get_quotes_by_category(category: str):
    filterQuote = [quote for quote in quotes_data if quote.get("category", "").lower() == category.lower()]
    if not filterQuote:
        return JSONResponse(content={"error": f"No quotes found for the category: {category}"})
    return JSONResponse(content=filterQuote)

# /quotes/randomAuthor    
@app.get('/quotes/randomAuthor')
def get_random_author():
    random_author = random.choice(quotes_data)
    if not random_author:
        return JSONResponse(content={"error": f"No quotes found for the category: {author}"})
    return JSONResponse(content=random_author)

# /quotes/authors
@app.get("quotes/authors")
def get_authors():
    author = [quote["author"] for quote in quotes_data]
    return JSONResponse(content=author)

# /quotes/categories
@app.get("quotes/categories")
def get_catgories():
    new_list = []
    for quote in quotes_data:
        if quote["category"] not in new_list:
            new_list.append(quote["category"])
    return JSONResponse(content=new_list)



# Model for the quote
class Quote(BaseModel):
    id: int
    author: str
    quote: str
    category: str


# Adding new quote
@app.post("/quotes/add", response_model=Quote)
async def add_quote(quote: Quote):
    if not quote.author:
        raise HTTPException(status_code=400, detail="Author is required")
    if not quote.quote:
        raise HTTPException(status_code=400, detail="Quote is required")
    if not quote.category:
        raise HTTPException(status_code=400, detail="Category is required")

    new_quote = {
        "id": len(quotes_data) + 1,  # Generate a unique ID for the quote
        "quote": quote.quote,
        "author": quote.author,
        "category": quote.category
    }
    quotes_data.append(new_quote)

    # Save data to the JSON file
    try:
        with open("quotes.json", "w") as file:
            json.dump(quotes_data, file, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving data to file: {str(e)}")

# /quotes/remove/11
@app.get("/quotes/remove/{id}")
async def remove_quote(id: int):
    filepath = 'quotes.json'
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail='Quotes file not found')
    
    try:
        with open(filepath, 'r') as fp:
            data = json.load(fp)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail='Error reading the quotes file')

    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail='Quotes file is not a valid list')
    
    # Find the quote with the specified ID
    quote_index = next((index for (index, d) in enumerate(data) if d.get("id") == id), None)

    if quote_index is None:
        raise HTTPException(status_code=404, detail='Quote ID not found')

    # Remove the quote from the list
    del data[quote_index]
    
    try:
        with open(filepath, 'w') as fp:
            json.dump(data, fp, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'An error occurred while saving the file: {str(e)}')

    return {"message": "Quote has been successfully deleted."}

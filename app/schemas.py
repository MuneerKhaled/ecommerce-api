from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# -------------------------
# Setup
# -------------------------

load_dotenv()

app = FastAPI(title="Book and Weather API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# In-memory storage
books: list[dict] = []
next_book_id = 1

# Simple weather cache: {city_lowercase: (expires_at, data)}
weather_cache: dict[str, tuple[datetime, dict]] = {}
CACHE_MINUTES = 10

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# -------------------------
# Models
# -------------------------

class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"
    reserved = "reserved"


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    author: str = Field(..., min_length=1, max_length=100)
    category: str = Field(default="general", max_length=50)
    status: BookStatus = BookStatus.available
    year: Optional[int] = Field(default=None, ge=0, le=datetime.now().year)


class BookUpdate(BaseModel):
    """All fields optional, used for PATCH (partial update)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = Field(default=None, max_length=50)
    status: Optional[BookStatus] = None
    year: Optional[int] = Field(default=None, ge=0, le=datetime.now().year)


class BorrowRequest(BaseModel):
    borrower: str = Field(..., min_length=1, max_length=100)
    days: int = Field(default=14, ge=1, le=60)


# -------------------------
# Helpers
# -------------------------

def find_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


def require_api_key():
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY is missing from .env")


async def fetch_weather(city: str) -> dict:
    """Fetch current weather, using a short-lived cache."""
    require_api_key()

    key = city.strip().lower()
    cached = weather_cache.get(key)
    if cached and cached[0] > datetime.now():
        return cached[1]

    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(WEATHER_URL, params=params)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Weather service unreachable")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    data = response.json()
    result = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
    }

    weather_cache[key] = (datetime.now() + timedelta(minutes=CACHE_MINUTES), result)
    return result


# -------------------------
# Frontend / Health
# -------------------------

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "time": datetime.now().isoformat(),
        "books_count": len(books),
        "api_key_loaded": bool(API_KEY),
    }


# -------------------------
# Weather API
# -------------------------

@app.get("/weather/{city}")
async def get_weather(city: str):
    return await fetch_weather(city)


@app.get("/weather/{city}/forecast")
async def get_forecast(city: str):
    """5-day forecast summarised as one entry per day."""
    require_api_key()

    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(FORECAST_URL, params=params)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Weather service unreachable")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    data = response.json()

    days: dict[str, list[dict]] = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        days.setdefault(date, []).append(item)

    forecast = []
    for date, items in days.items():
        temps = [i["main"]["temp"] for i in items]
        conditions = [i["weather"][0]["main"] for i in items]
        forecast.append({
            "date": date,
            "min_temp": round(min(temps), 1),
            "max_temp": round(max(temps), 1),
            "main_condition": max(set(conditions), key=conditions.count),
        })

    return {"city": data["city"]["name"], "forecast": forecast}


@app.get("/weather/{city}/reading-suggestion")
async def reading_suggestion(city: str):
    """Fun endpoint: suggests available books based on the weather."""
    weather = await fetch_weather(city)

    mood_map = {
        "Rain": ["fiction", "mystery", "poetry"],
        "Drizzle": ["fiction", "poetry"],
        "Thunderstorm": ["mystery", "horror", "thriller"],
        "Snow": ["fantasy", "fiction"],
        "Clear": ["adventure", "travel", "science"],
        "Clouds": ["general", "history", "biography"],
    }

    categories = mood_map.get(weather["condition"], ["general"])
    matches = [
        b for b in books
        if b["status"] == BookStatus.available.value
        and b["category"].lower() in categories
    ]

    return {
        "weather": weather,
        "suggested_categories": categories,
        "books": matches,
    }


# -------------------------
# Books - CREATE
# -------------------------

@app.post("/books", status_code=201)
def create_book(book: BookCreate):
    global next_book_id

    new_book = book.model_dump()
    new_book["status"] = book.status.value
    new_book["id"] = next_book_id
    new_book["borrower"] = None
    new_book["due_date"] = None
    new_book["created_at"] = datetime.now().isoformat()

    next_book_id += 1
    books.append(new_book)

    return new_book


# -------------------------
# Books - READ
# -------------------------

@app.get("/books")
def get_books(
    search: Optional[str] = Query(None, description="Search in title or author"),
    category: Optional[str] = None,
    status: Optional[BookStatus] = None,
    sort_by: str = Query("id", pattern="^(id|title|author|year)$"),
    descending: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    result = books

    if search:
        s = search.lower()
        result = [b for b in result if s in b["title"].lower() or s in b["author"].lower()]

    if category:
        result = [b for b in result if b["category"].lower() == category.lower()]

    if status:
        result = [b for b in result if b["status"] == status.value]

    result = sorted(
        result,
        key=lambda b: (b.get(sort_by) is None, b.get(sort_by) or ""),
        reverse=descending,
    )

    return {
        "total": len(result),
        "skip": skip,
        "limit": limit,
        "items": result[skip: skip + limit],
    }


@app.get("/books/stats")
def book_stats():
    by_status: dict[str, int] = {}
    by_category: dict[str, int] = {}

    for b in books:
        by_status[b["status"]] = by_status.get(b["status"], 0) + 1
        by_category[b["category"]] = by_category.get(b["category"], 0) + 1

    return {
        "total": len(books),
        "by_status": by_status,
        "by_category": by_category,
    }


@app.get("/books/overdue")
def overdue_books():
    now = datetime.now()
    return [
        b for b in books
        if b["due_date"] and datetime.fromisoformat(b["due_date"]) < now
    ]


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


# -------------------------
# Books - UPDATE
# -------------------------

@app.put("/books/{book_id}")
def replace_book(book_id: int, book: BookCreate):
    old_book = find_book(book_id)

    data = book.model_dump()
    data["status"] = book.status.value
    old_book.update(data)

    return old_book


@app.patch("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    old_book = find_book(book_id)

    changes = book.model_dump(exclude_unset=True)
    if "status" in changes and changes["status"] is not None:
        changes["status"] = changes["status"].value

    old_book.update(changes)
    return old_book


# -------------------------
# Books - Borrow / Return
# -------------------------

@app.post("/books/{book_id}/borrow")
def borrow_book(book_id: int, request: BorrowRequest):
    book = find_book(book_id)

    if book["status"] != BookStatus.available.value:
        raise HTTPException(status_code=400, detail=f"Book is {book['status']}")

    book["status"] = BookStatus.borrowed.value
    book["borrower"] = request.borrower
    book["due_date"] = (datetime.now() + timedelta(days=request.days)).isoformat()

    return book


@app.post("/books/{book_id}/return")
def return_book(book_id: int):
    book = find_book(book_id)

    if book["status"] != BookStatus.borrowed.value:
        raise HTTPException(status_code=400, detail="Book is not borrowed")

    book["status"] = BookStatus.available.value
    book["borrower"] = None
    book["due_date"] = None

    return book


# -------------------------
# Books - DELETE
# -------------------------

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    books.remove(book)
    return {"message": "Book deleted", "id": book_id}


@app.delete("/books")
def delete_all_books():
    count = len(books)
    books.clear()
    return {"message": f"{count} books deleted"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database import get_db

app = FastAPI(title="USA Toys Backend")

# CORS Configuration
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change to 'origins' list for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    # Database is initialized in database.py
    _ = get_db()
    print("Connected to MongoDB")

@app.get("/")
async def root():
    return {"message": "Welcome to USA Toys API"}

app.include_router(router)

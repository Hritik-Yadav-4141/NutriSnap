from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import nutrition, users

# Create all database tables
Base.metadata.create_all(bind=engine)

# This is the line the error is looking for
app = FastAPI(title="NutriVision AI")

# CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nutrition.router, prefix="/api/v1", tags=["Nutrition"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the NutriVision AI API!"}
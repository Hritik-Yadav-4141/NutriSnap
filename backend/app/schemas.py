from pydantic import BaseModel
from typing import List, Optional
import datetime

# This is the class that defines the nutritional info for one item
class NutritionInfo(BaseModel):
    food_name: str
    calories: float
    protein_g: float
    fat_g: float
    carbs_g: float

# This is the main response model the error is looking for
class ImagePredictionResponse(BaseModel):
    total_nutrition: NutritionInfo
    items: List[NutritionInfo]

# --- Schemas for User and Food Logs ---
class FoodLogBase(BaseModel):
    food_name: str
    calories: float

class FoodLogCreate(FoodLogBase):
    pass

class FoodLog(FoodLogBase):
    id: int
    owner_id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    food_logs: List[FoodLog] = []

    class Config:
        from_attributes = True
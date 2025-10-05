from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import Optional
from .. import schemas, crud
from ..utils import model_loader, nutrition_api
from ..database import get_db

router = APIRouter()

@router.post("/predict/", response_model=schemas.ImagePredictionResponse)
async def predict_nutrition_from_image(
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None), # Use Form for optional fields with files
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    image_bytes = await file.read()
    
    # 1. Get food items from the image using your AI model
    detected_items = model_loader.detect_food_items(image_bytes)

    if not detected_items:
        raise HTTPException(status_code=404, detail="No food items detected in the image.")

    # 2. Get nutrition data for each item and aggregate totals
    total_nutrition = schemas.NutritionInfo(food_name="Total", calories=0, protein_g=0, fat_g=0, carbs_g=0)
    item_details = []

    for item_name in detected_items:
        query = f"1 medium {item_name}"
        nutrition_info = nutrition_api.get_nutrition_details(query)
        
        if nutrition_info:
            total_nutrition.calories += nutrition_info.calories
            total_nutrition.protein_g += nutrition_info.protein_g
            total_nutrition.fat_g += nutrition_info.fat_g
            total_nutrition.carbs_g += nutrition_info.carbs_g
            item_details.append(nutrition_info)

    # 3. (Optional) Save the log to the database for the user
    if user_id:
        user = crud.get_user(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        log_entry = schemas.FoodLogCreate(
            food_name=", ".join(detected_items),
            calories=total_nutrition.calories
        )
        crud.create_user_food_log(db=db, food_log=log_entry, user_id=user_id)
        
    return {"total_nutrition": total_nutrition, "items": item_details}
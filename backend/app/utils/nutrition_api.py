import httpx
import os
from dotenv import load_dotenv
from .. import schemas

load_dotenv()

NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

# DEBUGGING: Let's read the keys from the environment
app_id = os.getenv("NUTRITIONIX_APP_ID")
api_key = os.getenv("NUTRITIONIX_API_KEY")

HEADERS = {
    'x-app-id': app_id,
    'x-app-key': api_key,
    'Content-Type': 'application/json'
}

def get_nutrition_details(query: str) -> schemas.NutritionInfo | None:
    print(f"Nutrition API: Fetching data for '{query}'...")

    # DEBUGGING: Print the keys to see if they loaded correctly
    print(f"--- DEBUG: Using App ID: {app_id}")
    print(f"--- DEBUG: Using API Key: {api_key}")

    if not app_id or not api_key:
        print("--- DEBUG ERROR: API ID or Key is missing from .env file or not loaded.")
        return None

    body = {"query": query}

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(NUTRITIONIX_API_URL, json=body, headers=HEADERS)

            # DEBUGGING: Print the raw response from the server
            print(f"--- DEBUG: Nutritionix API Status Code: {response.status_code}")
            print(f"--- DEBUG: Nutritionix API Response Body: {response.text}")

            response.raise_for_status()
            data = response.json()

            if data and "foods" in data and len(data["foods"]) > 0:
                food = data["foods"][0]
                return schemas.NutritionInfo(
                    food_name=food.get("food_name", "N/A"),
                    calories=food.get("nf_calories", 0),
                    protein_g=food.get("nf_protein", 0),
                    fat_g=food.get("nf_total_fat", 0),
                    carbs_g=food.get("nf_total_carbohydrate", 0),
                )
        return None
    except Exception as e:
        print(f"--- DEBUG An exception occurred: {e}")
        return None
from ultralytics import YOLO
import io
from PIL import Image

# Load the YOLOv8 model. 
# It will be downloaded automatically the first time this code runs.
# We use 'yolov8n.pt' - a small and fast version perfect for a hackathon.
model = YOLO('yolov8n.pt')

# Common food items from the COCO dataset which yolov8n.pt is trained on.
# This helps filter out non-food objects.
COCO_FOOD_ITEMS = ["apple", "banana", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "sandwich", "bowl", "cup"]

def detect_food_items(image_bytes: bytes) -> list[str]:
    """
    Detects food items in an image using a pre-trained YOLOv8 model.
    """
    print("AI Model: Running inference...")
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Run inference on the image
        results = model(image)
        
        detected_names = set() # Use a set to avoid duplicate items
        for r in results:
            for box in r.boxes:
                class_name = model.names[int(box.cls)]
                # Check if the detected object is in our list of food items
                if class_name in COCO_FOOD_ITEMS:
                    detected_names.add(class_name)
                    
        print(f"AI Model: Detected items - {list(detected_names)}")
        return list(detected_names)
        
    except Exception as e:
        print(f"An error occurred during model inference: {e}")
        return []
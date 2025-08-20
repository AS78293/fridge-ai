from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import numpy as np, cv2

from detect_food import detect_food_from_cv2
from spoonacular_client_min import search_recipes_simple

app = FastAPI()

# --- simple label normalizer so API gets good matches ---
BLOCKLIST = {"bottle", "container", "packet", "box"}
ALIASES = {
    "bell pepper": "red bell pepper",
    "capsicum": "green bell pepper",
    "tomatoes": "tomato",   
    "potatoes": "potato",
    "chilies": "chili pepper",
    "paneer": "cottage cheese",
    "curd": "yogurt",
}

def normalize_ingredients(labels):
    out = []
    for x in labels:
        x = x.strip().lower()
        if not x or x in BLOCKLIST: 
            continue
        x = ALIASES.get(x, x)
        out.append(x)
    # dedupe preserving order
    seen, final = set(), []
    for x in out:
        if x not in seen:
            seen.add(x); final.append(x)
    return final

# --- existing detect endpoint (kept) ---
@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if cv2_img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    items = detect_food_from_cv2(cv2_img)
    return {"detected_items": normalize_ingredients(items)}

# --- recipes from ingredient list ---
class RecipesRequest(BaseModel):
    ingredients: list[str]
    vegetarian: bool = False
    top_k: int = 5

@app.post("/recipes")
def recipes(payload: RecipesRequest):
    ings = normalize_ingredients(payload.ingredients)
    if not ings:
        raise HTTPException(status_code=400, detail="No valid ingredients")
    try:
        recs = search_recipes_simple(ings, veg_only=payload.vegetarian, top_k=payload.top_k)
        return {"ingredients_used": ings, "recipes": recs}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Recipe API error: {e}")

# --- one-shot: upload image -> detect -> recipes ---
@app.post("/detect_and_recipes")
async def detect_and_recipes(file: UploadFile = File(...), vegetarian: bool = False, top_k: int = 5):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if cv2_img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    detected = normalize_ingredients(detect_food_from_cv2(cv2_img))
    if not detected:
        return {"detected_items": [], "recipes": []}

    try:
        recs = search_recipes_simple(detected, veg_only=vegetarian, top_k=top_k)
        return {"detected_items": detected, "recipes": recs}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Recipe API error: {e}")

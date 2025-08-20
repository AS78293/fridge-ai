import requests

API_KEY = "d1d981da6fe5497d8db3e028c8848b9f" 
BASE = "https://api.spoonacular.com"

def search_recipes_simple(ingredients, veg_only=False, top_k=5, timeout=20):
    import requests

    API_KEY = "d1d981da6fe5497d8db3e028c8848b9f"
    BASE = "https://api.spoonacular.com"

    params = {
        "includeIngredients": ",".join(ingredients[:10]),
        "number": top_k,
        "addRecipeInformation": True,
        "instructionsRequired": True,
        "sort": "max-used-ingredients",
        "apiKey": API_KEY,
    }
    if veg_only:
        params["diet"] = "vegetarian"

    r = requests.get(f"{BASE}/recipes/complexSearch", params=params, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    results = data.get("results", [])

    # Expanded version (equivalent to the list comprehension)
    cleaned = []
    for rec in results:
        cleaned.append({
            "id": rec.get("id"),
            "title": rec.get("title"),
            "image": rec.get("image"),
            "readyInMinutes": rec.get("readyInMinutes"),
            "servings": rec.get("servings"),
            "sourceUrl": rec.get("sourceUrl"),
            "vegetarian": rec.get("vegetarian"),
            "usedIngredientCount": rec.get("usedIngredientCount"),
            "missedIngredientCount": rec.get("missedIngredientCount"),
        })

    return cleaned

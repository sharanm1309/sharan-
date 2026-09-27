import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import (
    save_user, save_plan, update_plan,
    get_original_plan, get_all_users_with_plans,
)

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# 1. Home route - shows the input form
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 2. Generate a personalized workout plan + nutrition tip
@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        plan = generate_workout_gemini({"goal": goal, "intensity": intensity})
        nutrition_tip = generate_nutrition_tip_with_flash(goal)

        save_user(user_id, username, age, weight, goal, intensity)
        save_plan(user_id, plan, nutrition_tip)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": plan,
            "nutrition_tip": nutrition_tip,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


# 3. Submit feedback and update the plan
@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    feedback: str = Form(...),
):
    original = get_original_plan(user_id)
    if not original:
        raise HTTPException(status_code=404, detail="Original plan not found for this user.")

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "workout_plan": updated,
        "nutrition_tip": nutrition_tip,
        "updated": True,
    })


# 4. Admin dashboard - view all users & their plans
@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    users = get_all_users_with_plans()
    return templates.TemplateResponse("all_users.html", {"request": request, "users": users})


# ---- JSON API endpoints (for /docs testing) ----

@router.post("/api/generate-workout")
def api_generate_workout(goal: str, intensity: str):
    plan = generate_workout_gemini({"goal": goal, "intensity": intensity})
    return {"model": "gemini-1.5-pro", "workout_plan": plan}


@router.get("/api/nutrition-tip")
def api_nutrition_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}

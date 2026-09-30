# Epic 3: App.py Development

This epic builds the routing logic, the core operational layer of FitBuddy. It bridges the frontend templates, the AI generation modules (Gemini Pro and Flash) and the SQLite database. In the project structure this logic sits in the `app/` package (`main.py` entry point and `routes.py` handlers).

## 3.1 Writing the Main Application Logic

**Core routes**
1. `/` – displays the user form (index.html)
2. `/generate-workout` – processes input and generates a personalized plan
3. `/submit-feedback` – updates the plan based on feedback
4. `/view-all-users` – admin dashboard of all users and plans

**Route handlers**

`/` (Home) – returns index.html; no form processing.

`/generate-workout` (Plan Generator)
- Receives input via `Form(...)` and builds a `UserInput` Pydantic model
- Calls `generate_workout_gemini(...)` (Gemini 1.5 Pro) and `generate_nutrition_tip_with_flash(...)` (Gemini Flash)
- Stores user details with `save_user(...)` and the plan with `save_plan(...)`
- Returns result.html with dynamic data

`/submit-feedback` (Update Plan)
- Captures feedback and user_id, retrieves the original plan from the DB
- Uses `update_workout_plan(...)` (Gemini 1.5 Pro) to revise it
- Saves the result with `update_plan(...)` and renders result.html

`/view-all-users` (Admin View)
- Calls `get_all_users()` and `get_all_plans()`, passes them to all_users.html
- Admin sees username, age, weight, goal, intensity, and original and updated plans

**Gemini responses in each function:** workout generation and plan updates use Gemini Pro; nutrition tips use Gemini Flash. All responses are shown through result.html using `<pre>` blocks for formatting.

**Route code**

```python
# 1. API: Generate workout using Gemini Pro
@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. API: Generate nutrition tip using Gemini Flash
@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}

# 3. API: Save user info & generate plan
@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id, name=user_data.username,
            age=user_data.age, weight=user_data.weight,
            goal=user_data.goal, intensity=user_data.intensity
        )
        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity
        })
        save_plan(user_data.user_id, plan)
        return {"message": "Workout plan generated and saved successfully!",
                "workout_plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")

# 4. API: Update workout plan based on user feedback
@router.post("/update-plan/{user_id}", response_model=dict)
def update_user_plan(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}
    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}
```

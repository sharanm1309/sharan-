# Epic 2: Core Functionalities Development

## 2.1 Develop the Core Functionalities

### Workout Plan Generation
Function `generate_workout_gemini()` in `gemini_generator.py` builds a personalized 7-day plan from goal and intensity using Gemini 1.5 Pro. Each day includes a warm-up (5–10 mins), main workout (exercises, sets, reps) and a cooldown or recovery tip. Output is returned to routes.py and rendered in result.html inside `<pre>` blocks.

```python
def generate_workout_gemini(user_input):
    prompt = f"""
    You are a professional fitness trainer.

    Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**, and prefers **{user_input['intensity']}** intensity workouts.

    Each day must include:
    - A warm-up (5-10 min)
    - Main workout (targeted exercises, sets & reps)
    - Cooldown or recovery tip

    Format:
    Day 1:
    Warm-up: ...
    Main Workout: ...
    Cooldown: ...
    (Repeat for Day 2-7)
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
```

### Nutrition Tip Generation
Function `generate_nutrition_tip_with_flash()` in `gemini_flash_generator.py` uses Gemini Flash to return one concise, practical tip for the user's goal ("weight loss", "muscle gain" or "general fitness"). It is displayed beneath the plan in result.html.

```python
def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating tip: {str(e)}"
```

### Feedback-Based Plan Updating
Function `update_workout_plan()` in `updated_plan.py` passes the original plan and user feedback (e.g. "Add yoga", "Include more cardio") to Gemini 1.5 Pro, which returns a modified plan. The updated plan is stored and displayed with the new tip.

```python
def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    prompt = f"""
    You are a professional fitness trainer assistant.

    Here's the original 7-day workout plan:
    {original_plan}

    User Feedback:
    "{user_feedback}"

    Based on the feedback, revise the relevant parts of the workout plan. Keep the format and rest of the plan unchanged if not needed.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error updating plan: {e}"
```

### User & Plan Storage (`database.py`)
Functions: `save_user()`, `save_plan()`, `update_plan()`, `get_original_plan()`, `get_user()`. User info (ID, name, age, weight, goal, intensity) and plans are stored in SQLite via SQLAlchemy. Feedback updates go into a separate field so both the original and updated versions are preserved.

```python
def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    existing = db.query(User).filter_by(id=user_id).first()
    if existing:
        existing.name = name
        existing.age = age
        existing.weight = weight
        existing.goal = goal
        existing.intensity = intensity
    else:
        user = User(id=user_id, name=name, age=age, weight=weight,
                    goal=goal, intensity=intensity, schedule=7)
        db.add(user)
    db.commit()
    db.close()

def save_plan(user_id: int, plan: str):
    db = SessionLocal()
    workout = WorkoutPlan(user_id=user_id, original_plan=plan)
    db.add(workout)
    db.commit()
    db.close()

def update_plan(user_id: int, updated_text: str):
    db = SessionLocal()
    workout = db.query(WorkoutPlan).filter_by(user_id=user_id).first()
    if workout:
        workout.updated_plan = updated_text
        db.commit()
    db.close()

def get_original_plan(user_id: int):
    db = SessionLocal()
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
    return plan.original_plan if plan else None

def get_user(user_id: int):
    db = SessionLocal()
    return db.query(User).filter(User.id == user_id).first()
```

### Admin View of All Users
Route `/view-all-users`, template `all_users.html`. Lists all users with their original and updated plans in a table using a Jinja2 `{% for user in users %}` loop.

```python
@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    user_data = []
    for user in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_data.append({
            "id": user.id, "name": user.name, "age": user.age,
            "weight": user.weight, "goal": user.goal, "intensity": user.intensity,
            "original_plan": plan.original_plan if plan else "N/A",
            "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated"
        })
    db.close()
    return templates.TemplateResponse("all_users.html", {"request": request, "users": user_data})
```

## 2.2 Implement the FastAPI Backend to Manage Routing and User Input Processing

- **Routes:** all routing logic lives in routes.py, each route linked to a function from 2.1.
- **User input:** the HTML form in index.html collects username, user_id, age, weight, goal and intensity. FastAPI captures them with `Form(...)`; Pydantic schemas (`UserInput`, `FeedbackRequest`) validate structure.
- **Gemini integration:**
  - `/generate-workout` → `generate_workout_gemini()` for the plan and `generate_nutrition_tip_with_flash()` for the tip
  - `/submit-feedback` → retrieves the plan and sends original + feedback to `update_workout_plan()`

AI responses are returned and injected into the frontend templates for display.

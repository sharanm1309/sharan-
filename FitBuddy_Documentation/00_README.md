# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a web-based application that uses AI to generate personalized workout plans and nutrition tips based on a user's fitness goals (weight loss, muscle gain, general wellness). It is built with FastAPI and Google's Gemini models, with SQLite for storage.

The app takes user information (name, age, weight, goal, preferred intensity) and generates a customized 7-day plan. Users can submit feedback to refine the plan, and a nutrition or recovery tip is provided for their goal. It offers both API endpoints and an interactive HTML interface.

## Scenarios
1. **Plan generation** – User enters name, age, weight, goal and intensity (high / medium / low) and receives a personalized 7-day plan.
2. **Feedback** – User submits feedback such as "more focus on cardio" or "include more rest days"; the plan is regenerated.
3. **Nutrition tip** – User receives a concise nutrition/recovery tip for their goal (e.g. protein after workouts for muscle gain).
4. **Admin view** – Admin/coach views all users with original and updated plans.

## Technical Architecture
User (Browser) → FastAPI Backend (app/main.py) → three branches:
- HTML templating (Jinja2 + CSS): index.html (form)
- Workout logic (routes.py + AI): result.html (plan page) → Gemini 1.5 Pro & Gemini Flash → AI Plan/Nutrition Generator (updated_plan.py) → SQLite + SQLAlchemy (fitbuddy.db: users, plans)
- Admin panel (/view-all-users): all_users.html

## Contents
1. Pre-Requisites
2. Project Workflow
3. Epic 1: Model Selection and Architecture
4. Epic 2: Core Functionalities Development
5. Epic 3: App.py Development
6. Epic 4: Frontend Development
7. Epic 5: Deployment
8. Conclusion

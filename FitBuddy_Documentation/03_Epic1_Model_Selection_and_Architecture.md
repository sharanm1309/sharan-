# Epic 1: Model Selection and Architecture

This epic selects the appropriate generative AI models from Google's Gemini family for FitBuddy, evaluating them against the core functions: generating personalized workout plans, updating them from feedback, and providing tailored nutrition or recovery advice.

## 1.1 Research and Select the Appropriate Generative AI Model

**Requirements** – the model needed to:
- Generate structured 7-day workout plans
- Provide concise and actionable nutrition tips
- Update workout plans based on user feedback
- Perform well in real-time, web-based interaction

**Model evaluation** – Hugging Face models were tried first:
- T5 & BART – text generation (workout/nutrition)
- DistilBERT – potential intent classification
- Bloom – general-purpose generation

They showed promise but required hosting with Hugging Face or a local GPU setup, and fine-tuning or complex prompting to get structured plans.

**Final selection** – Google Gemini models:
- **Gemini 1.5 Pro** – structured 7-day workout generation and plan updating; rich, context-aware, reliably formatted responses.
- **Gemini Flash** – fast, practical nutrition tips; lightweight and efficient for quick API calls.

**Why Gemini:** API-based and easy to integrate with FastAPI; naturally understands structured formatting (days, sections); high accuracy with minimal prompt tuning; scalable and fast for feedback-based revisions.

## 1.2 Define the Architecture of the Application

FitBuddy follows a modular FastAPI-based architecture:
- **Frontend:** HTML + Jinja2 templates for input and display
- **Backend:** FastAPI for route handling and logic
- **AI layer:** Google Gemini APIs (Pro & Flash)
- **Database:** SQLite with SQLAlchemy

**Frontend responsibilities:** index.html (input form), result.html (plan, tip, feedback), all_users.html (admin panel).

**Backend responsibilities:** receive form data, call Gemini models, store user info and plans, render dynamic templates.

**AI integration points:** workout generation and feedback updates → Gemini Pro; nutrition tips → Gemini Flash.

## 1.3 Set Up the Development Environment

1. Install Python and pip.
2. Create a virtual environment:
   ```
   python -m venv fitbuddy-env
   fitbuddy-env\Scripts\activate      (Windows)
   ```
3. Install libraries:
   ```
   pip install fastapi uvicorn jinja2 sqlalchemy python-multipart google-generativeai
   ```
4. Run the server:
   ```
   uvicorn app.main:app --reload
   ```
   Visit http://127.0.0.1:8000 for the app and /docs for API testing.

**Project structure**
```
fitbuddy/
├── requirements.txt
├── app/
│   ├── main.py                    # FastAPI entry point
│   ├── routes.py                  # Core route handlers
│   ├── database.py                # SQLAlchemy models and DB logic
│   ├── schemas.py                 # Pydantic models for validation
│   ├── gemini_generator.py        # Gemini Pro - workout plan generator
│   ├── gemini_flash_generator.py  # Gemini Flash - nutrition tips
│   ├── updated_plan.py            # Feedback-based plan updater
│   ├── nutrition.py               # Nutrition-specific logic (optional)
│   ├── templates/
│   │   ├── index.html
│   │   ├── result.html
│   │   └── all_users.html
│   └── static/images/gym-bg.jpg
└── fitbuddy.db                    # Local SQLite database (auto-generated)
```

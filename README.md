# FitBuddy – AI Fitness Plan Generator

## How to run

1. Create a virtual environment
   ```
   python -m venv fitbuddy-env
   fitbuddy-env\Scripts\activate        # Windows
   source fitbuddy-env/bin/activate     # Mac/Linux
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Add your Gemini API key
   - Copy `.env.example` to `.env`
   - Get a free key at https://aistudio.google.com/app/apikey
   - Paste it into `.env`: `GOOGLE_API_KEY=your_key_here`

4. Run the server (from the project root, the folder containing `app/`)
   ```
   uvicorn app.main:app --reload
   ```

5. Open in your browser
   - App: http://127.0.0.1:8000
   - Admin view: http://127.0.0.1:8000/view-all-users
   - API docs: http://127.0.0.1:8000/docs

## Project structure
```
fitbuddy/
├── requirements.txt
├── .env.example
└── app/
    ├── main.py                    # FastAPI entry point
    ├── routes.py                  # All routes
    ├── database.py                # SQLAlchemy models + DB logic
    ├── schemas.py                 # Pydantic models
    ├── gemini_generator.py        # Gemini 1.5 Pro – workout plans
    ├── gemini_flash_generator.py  # Gemini Flash – nutrition tips
    ├── updated_plan.py            # Feedback-based plan updater
    ├── templates/                 # index.html, result.html, all_users.html
    └── static/images/
```

Note: this code was syntax-checked in the build sandbox (no live internet there),
so it couldn't be run end-to-end against the real Gemini API in this environment.
Once you add a valid `GOOGLE_API_KEY` and run it locally, it will work as described above.

# Epic 5: Deployment

This epic deploys FitBuddy on a local system using FastAPI and Uvicorn, ensuring dependencies are installed and the app runs smoothly, in preparation for future cloud deployment.

## 5.1 Preparing the Application for Local Deployment

**Virtual environment**
```
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
requirements.txt includes FastAPI, Uvicorn, SQLAlchemy and the Google Generative AI SDK.

**Environment variables** – store sensitive data such as the Gemini API key in the terminal environment or in a `.env` file loaded with python-dotenv:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Frontend-backend rendering via Jinja2:** index.html collects inputs, result.html displays the generated plan, all_users.html lists all user records for the admin view.

## 5.2 Testing and Verifying Local Deployment

**Access locally** – start the server with `uvicorn main:app --reload`, then open http://127.0.0.1:8000 for the main UI. Interactive API docs are at http://127.0.0.1:8000/docs.

**Home page** – a form with Name, User ID, Age, Weight (kg), Fitness Goal (e.g. weight loss, flexibility) and Workout Intensity (Low, Medium, High). The "Generate Plan" button triggers the AI backend to create a customized plan; a fitness-themed background reinforces the purpose.

**Personalized workout page**
- *User Information:* summary of Name, User ID, Age, Weight, Fitness Goal and Intensity.
- *Workout Plan:* a day-wise plan with a clear focus per day (upper body, lower body, HIIT cardio, active recovery), exercises with sets and reps, warm-up and cooldown guidance, and closing notes on progressive overload, form, listening to your body, nutrition and hydration.
- *Nutrition Tip:* concise dietary advice, e.g. prioritize protein at every meal (chicken, fish, beans, Greek yogurt) for muscle building, satiety and metabolism.

**Feedback page** – the user enters their unique User ID and feedback on effectiveness, difficulty or preferences. The system updates the plan and shows a confirmation: "Your plan has been updated based on your feedback!"

**View all users page** – an admin table of all users (ID, name, age, weight, goal, intensity) with the original plan beside the updated plan, showing how each plan evolved after feedback.

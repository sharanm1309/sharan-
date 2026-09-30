# Epic 4: Frontend Development

This epic builds a user-friendly, visually structured interface using HTML, CSS and Jinja2. Each template is rendered dynamically through FastAPI so users can submit input, receive plans, give feedback, and administrators can manage data.

## 4.1 Designing and Developing the User Interface

**Base HTML structure**
- index.html is the main entry point; the form captures username, user_id, age, weight, goal and intensity.
- Fields are labeled and grouped with semantic HTML.
- Gym-themed background image, Google Fonts (Roboto) and bold typography give a clean fitness look.
- Navigation is minimal; flow goes from input to output.

**Responsive layout with CSS**
- Embedded CSS in each HTML file
- Flexbox centers content vertically and horizontally
- Media queries for mobile responsiveness
- Consistent button styling with hover effects
- Padding, shadows and rounded corners on inputs and result blocks
- Color scheme readable on a dark background

**Separate pages (under /templates)**
- **index.html** – input form (goal, intensity, personal info)
- **result.html** – 7-day AI plan, nutrition tip, and feedback form
- **all_users.html** – admin panel to view and delete users and review original and updated plans

Templates are modular, transitions between steps are smooth, and forms are submitted to FastAPI endpoints via POST.

## 4.2 Creating Dynamic Templates with FastAPI's Jinja2

**Jinja2 setup**
```python
from fastapi.templating import Jinja2Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)
```

**Rendering with context**
```python
return templates.TemplateResponse("result.html", {
    "request": request,
    "username": username,
    "user_id": user_id,
    "age": age,
    "weight": weight,
    "goal": goal,
    "intensity": intensity,
    "workout_plan": plan,
    "nutrition_tip": nutrition_tip
})
```

**Binding backend data to templates**
- **index.html** – form elements use `name="..."` to bind to backend `Form(...)` parameters; submits to `/generate-workout`.
- **result.html** – shows `{{ username }}`, `{{ goal }}`, `{{ intensity }}` etc., plus `{{ workout_plan }}` and `{{ nutrition_tip }}`; includes a feedback form POSTing to `/submit-feedback`.
- **all_users.html** – loops over all user records:
```html
{% for user in users %}
<tr>
    <td>{{ user.id }}</td>
    <td>{{ user.name }}</td>
    <td>{{ user.age }}</td>
    <td>{{ user.weight }}</td>
    <td>{{ user.goal }}</td>
    <td>{{ user.intensity }}</td>
    <td><pre>{{ user.original_plan }}</pre></td>
    <td><pre>{{ user.updated_plan }}</pre></td>
</tr>
{% endfor %}
```

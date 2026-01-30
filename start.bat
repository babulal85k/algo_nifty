python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

start cmd /k uvicorn web.backend.api:app --port 8000
start cmd /k python main.py
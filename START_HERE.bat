@echo off
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
where %PY% >nul 2>nul || (echo Python was not found. Install it from python.org and tick Add Python to PATH. & pause & exit /b)
if not exist venv (%PY% -m venv venv)
call venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
pause

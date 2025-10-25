@echo off
echo Starting MySite Django Development Server...
echo.
echo Make sure you have activated your virtual environment first!
echo.
echo If you haven't created a virtual environment yet:
echo 1. python -m venv venv
echo 2. venv\Scripts\activate
echo 3. pip install -r requirements.txt
echo 4. python manage.py migrate
echo.
echo Starting server...
python manage.py runserver
pause







@echo off
REM Setup and run the RFP Management System locally (Windows)

echo 🚀 AI-Powered RFP Management System - Setup Script (Windows)
echo ===========================================================
echo.

REM Check prerequisites
echo ✓ Checking prerequisites...
python --version >nul 2>&1 || (echo Python is required but not installed. & exit /b 1)
node --version >nul 2>&1 || (echo Node.js is required but not installed. & exit /b 1)
npm --version >nul 2>&1 || (echo npm is required but not installed. & exit /b 1)

echo ✓ Python installed
echo ✓ Node installed
echo ✓ npm installed
echo.

REM Backend Setup
echo 📦 Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo   Installing Python dependencies...
pip install -q -r requirements.txt

REM Setup environment variables
if not exist ".env" (
    echo   Creating .env file...
    copy .env.example .env
    echo   ⚠️  Please update .env with your credentials:
    echo      - OPENAI_API_KEY
    echo      - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
    echo      - MONGODB_URI (if not local)
)

cd ..
echo ✓ Backend setup complete
echo.

REM Frontend Setup
echo 📦 Setting up frontend...
cd frontend

REM Install dependencies
echo   Installing npm dependencies...
call npm install -q

cd ..
echo ✓ Frontend setup complete
echo.

echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo.
echo 1. Configure credentials:
echo    Edit backend\.env with your:
echo    - OPENAI_API_KEY (from https://platform.openai.com/api-keys)
echo    - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
echo    - MONGODB_URI (if using MongoDB Atlas)
echo.
echo 2. Start services (in separate terminals):
echo.
echo    Terminal 1 - Backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python manage.py runserver
echo.
echo    Terminal 2 - Frontend:
echo    cd frontend
echo    npm start
echo.
echo    Terminal 3 - Database (if local MongoDB):
echo    mongod
echo.
echo 3. Access the application:
echo    Frontend: http://localhost:4200
echo    Backend API: http://localhost:8000/api/
echo.
echo 4. (Optional) Seed sample vendors:
echo    cd backend
echo    python manage.py seed_vendors
echo.
echo 📚 Documentation:
echo    - QUICKSTART.md - 5-minute setup guide
echo    - README.md - Complete documentation
echo    - API_EXAMPLES.md - API usage examples
echo    - ARCHITECTURE.md - System design
echo.
pause

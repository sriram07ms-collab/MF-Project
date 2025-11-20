@echo off
echo ====================================
echo Starting Frontend Server
echo ====================================
cd frontend

REM Install dependencies if needed
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

REM Create .env.local if needed
if not exist .env.local (
    echo Creating .env.local...
    echo NEXT_PUBLIC_API_BASE=http://localhost:8000 > .env.local
)

REM Start dev server
echo.
echo Starting frontend server on http://localhost:3000
echo Press Ctrl+C to stop
echo.
call npm run dev
pause




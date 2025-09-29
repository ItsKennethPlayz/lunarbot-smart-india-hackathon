@echo off
REM Lunarbot Document Converter - Windows Batch Script
REM Converts markdown to DOC and PDF formats

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   🚀 LUNARBOT CONVERTER 🚀                     ║
echo ║              Smart India Hackathon Document Converter         ║
echo ║                                                                ║
echo ║    Converting Markdown to DOC ^& PDF like a space wizard!     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo    Please run: python -m venv .venv
    echo    Then run: .venv\Scripts\activate
    echo    Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment and run converter
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 🚀 Starting conversion process...
python convert_all.py %*

echo.
echo ✨ Conversion complete! Check the output files.
echo.
pause

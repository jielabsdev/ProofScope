@echo off
python "%~dp0mock_engine.py" %*
exit /b %ERRORLEVEL%

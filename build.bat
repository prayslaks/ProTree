@echo off
  setlocal

  echo [1/3] Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
      echo ERROR: Failed to create virtual environment.
      exit /b 1
  )

  echo [2/3] Installing dependencies...
  .venv\Scripts\pip install -r requirements.txt --quiet
  if errorlevel 1 (
      echo ERROR: pip install failed.
      exit /b 1
  )

  echo [3/3] Building protree.exe...
  .venv\Scripts\pyinstaller --onefile --name protree --distpath dist --workpath build\pyinstaller --specpath build\pyinstaller protree.py
  if errorlevel 1 (
      echo ERROR: PyInstaller build failed.
      exit /b 1
  )

  echo.
  echo Build complete: %~dp0dist\protree.exe
  echo.

  :: --- 선택적 설치 ---
  set INSTALL_DIR=%USERPROFILE%\tools
  set /p INSTALL="Install to %INSTALL_DIR% and add to PATH? [y/N] "
  if /i not "%INSTALL%"=="y" goto :done

  if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
  copy /y "%~dp0dist\protree.exe" "%INSTALL_DIR%\protree.exe" >nul

  :: User PATH에 이미 있는지 확인 후 추가
  echo %PATH% | find /i "%INSTALL_DIR%" >nul
  if errorlevel 1 (
      setx PATH "%USERPROFILE%\tools;%PATH%"
      echo Added %INSTALL_DIR% to user PATH.
      echo Restart your terminal to apply.
  ) else (
      echo %INSTALL_DIR% is already in PATH.
  )

  :done
  endlocal

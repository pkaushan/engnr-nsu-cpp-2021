cd ".github/functional-testing"                             || exit /b 1

python3 --version                                           || exit /b 1

@echo.
@echo ======================== Functional testing of x86_32 ========================
@echo.                             x86_32 (Debug)
python3 main.py "..\..\%LAB_INDEX%\build\x86_32" "--config=Debug"   || exit /b 1
@echo.
@echo x86_32 Debug: ok.
@echo.
@echo.                            x86_32 (Release)
python3 main.py "..\..\%LAB_INDEX%\build\x86_32" "--config=Release" || exit /b 1
@echo.
@echo x86_32 Release: ok.
@echo.

@echo.
@echo x86_32: ok.
@echo ==============================================================================

@echo.
@echo.

@echo ======================== Functional testing of x86_64 ========================
@echo.                             x86_64 (Debug)
python3 main.py "..\..\%LAB_INDEX%\build\x86_64" "--config=Debug"     || exit /b 1
@echo.
@echo x86_64 Debug: ok.
@echo.
@echo.                            x86_64 (Release)
python3 main.py "..\..\%LAB_INDEX%\build\x86_64" "--config=Release"   || exit /b 1
@echo.
@echo x86_64 Release: ok.
@echo.

@echo.
@echo x86_64: ok.
@echo ==============================================================================

@echo.
@echo.

@echo Passed.
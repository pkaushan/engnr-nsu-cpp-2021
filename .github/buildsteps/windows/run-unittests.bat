cd "%LAB_INDEX%"    || exit /b 1

cd "build"          || exit /b 1

ctest --version

@echo.
@echo ======================== Unit testing of x86_32 =========================
cd "x86_32"         || exit /b 1
@echo.                             x86_32 (Debug)
ctest -C Debug      || exit /b 1
@echo.
@echo.                            x86_32 (Release)
ctest -C Release    || exit /b 1
cd ".."             || exit /b 1

@echo.
@echo x86_32: ok.
@echo =========================================================================

@echo.
@echo.

@echo ======================== Unit testing of x86_64 =========================
cd "x86_64"         || exit /b 1
@echo.                             x86_64 (Debug)
ctest -C Debug      || exit /b 1
@echo.
@echo.                            x86_64 (Release)
ctest -C Release    || exit /b 1
cd ".."             || exit /b 1

@echo.
@echo x86_64: ok.
@echo =========================================================================

@echo.
@echo.

@echo Passed.
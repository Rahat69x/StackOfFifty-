@echo off
title AegisCore C++20 Build
echo =======================================================
echo        Compiling AegisCore Native C++20 Server
echo =======================================================

echo [*] Compiling main.cpp with g++...
g++ -std=c++20 -O2 main.cpp -lws2_32 -liphlpapi -lpsapi -o aegiscore_server.exe

if %ERRORLEVEL% EQU 0 (
    echo [+] Compilation SUCCESS! Output: aegiscore_server.exe
) else (
    echo [-] Compilation Failed!
)

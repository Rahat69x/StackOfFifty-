@echo off
title StackOfFifty C++20 Build
echo =======================================================
echo        Compiling StackOfFifty Native C++20 Server
echo =======================================================

echo [*] Compiling main.cpp with g++...
g++ -std=c++20 -O2 main.cpp -lws2_32 -liphlpapi -lpsapi -o stackoffifty_server.exe

if %ERRORLEVEL% EQU 0 (
    echo [+] Compilation SUCCESS! Output: stackoffifty_server.exe
) else (
    echo [-] Compilation Failed!
)

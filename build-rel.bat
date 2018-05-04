@echo off
pushd src && tools\compile-gui && python tools\build.py && popd && xcopy /y src\dist\turing.exe . && gen-arc

@echo off
pushd src && tools\compile-gui && tools\build && popd && xcopy /y src\dist\*.exe . && gen-arc

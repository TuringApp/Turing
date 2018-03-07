@echo off
for %%f in (*.ui) do pyuic5 %%f -o %%~nf.py

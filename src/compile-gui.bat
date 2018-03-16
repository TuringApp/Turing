@echo off
for %%f in (*.ui) do pyuic5 %%f -o %%~nf.py
pylupdate5 project.pro
pushd lang
for %%f in (*.ts) do lrelease %%f
popd
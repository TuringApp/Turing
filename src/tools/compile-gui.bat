@echo off
pushd forms
for %%f in (*.ui) do pyuic5 %%f -o %%~nf.py
popd
pushd tools
python progen.py
popd tools
pylupdate5 project.pro
pushd lang
for %%f in (*.ts) do lrelease %%f
popd
pyrcc5 turing.qrc -o turing_rc.py
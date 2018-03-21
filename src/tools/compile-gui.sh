#!/bin/bash

cd forms

for f in *.ui;
do
    pyuic5 $f -o ${f%.*}.py;
done

cd ..

cd tools

python3 progen.py

cd ..

pylupdate5 project.pro

cd lang

for f in *.ts;
do
    lrelease $f;
done

cd ..

pyrcc5 turing.qrc -o turing_rc.py

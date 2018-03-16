#!/bin/bash

for f in *.ui;
do
    pyuic5 $f -o ${f%.*}.py;
done

pylupdate5 project.pro

cd lang

for f in *.ts;
do
    lrelease $f;
done

cd ..
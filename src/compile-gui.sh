#!/bin/bash

for f in *.ui;
do
	pyuic5 $f -o ${f%.*}.py;
done


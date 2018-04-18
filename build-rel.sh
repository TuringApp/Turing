#!/bin/bash

cd src

tools/compile-gui.sh
python3 tools/build.py

cd ..

\cp src/dist/* .

./gen-arc.sh

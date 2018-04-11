#!/bin/bash

cd src

tools/compile-gui.sh
tools/build.sh

cd ..

\cp src/dist/* .

./gen-arc.sh

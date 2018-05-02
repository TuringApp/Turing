#!/bin/bash

version=$(grep -oP '__version__ = "[^\d]*\K[^"]+' src/main.py)

tar -cvzf Turing-$version-nix64.tar.gz examples editor_backend turing

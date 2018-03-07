# Turing

Turing is a free and cross-platform app whose main goal is to assist the learning of algorithms and programming languages by providing easy-to-use development tools to all.

It provides a lighter alternative to the well-known Algobox, which is the currently de-facto widely used solution.

## Quid, quis, quomodo?

Turing is written in Python 3 and uses the PyQt5 framework for its GUI. It provides two work modes:

- Algorithm mode
  - Uses a "natural" pseudocode language similar to the one used in Algobox and school books.
  - Assisted development
- Program mode
  - Uses Python, for the more experienced

In both modes, the code can be debugged and executed step-by-step to facilitate the problem-solving side of development.

## Using Turing

Turing is cross-platform, but has only been tested on Windows and Linux-based operating systems. macOS should be supported, but no guarantee is made of that.

First, install the latest version of Python 3 [available here](https://www.python.org/downloads/), and install PyQt5 using pip:

    pip install PyQt5

Note: if you have Python 2.x installed on your computer, the old `pip` may be present in `PATH` and interfere with the above command line. If that happens, try using `pip3` instead of `pip`.

Next, open the src/ folder and either double-click on `main.py` or call `python main.py` from a command line.


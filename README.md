[![GitHub issues](https://img.shields.io/github/issues/TuringApp/Turing.svg)](https://github.com/TuringApp/Turing/issues) [![GitHub stars](https://img.shields.io/github/stars/TuringApp/Turing.svg)](https://github.com/TuringApp/Turing/stargazers) [![GitHub license](https://img.shields.io/github/license/TuringApp/Turing.svg)](https://github.com/TuringApp/Turing/blob/master/LICENSE) [![Gitter](https://img.shields.io/gitter/room/TuringDevelopment/Lobby.svg)]( https://gitter.im/TuringDevelopment)

# Turing

Turing is a free and cross-platform app whose main goal is to assist the learning of algorithms and programming languages by providing easy-to-use development tools to all.

It provides a lighter alternative to the well-known Algobox, which is the currently de-facto widely used solution.

**Note:** Turing was originally meant to be a school project for the [CS class](https://twitter.com/davR74130). Don't expect enterprise-grade code here. We do our best to keep the whole codebase clean, but some parts are still undocumented and not covered by unit tests.

## Quid, quis, quomodo?

Turing is written in Python 3.6 and uses the PyQt5 framework for its GUI. It provides two work modes:

- Algorithm mode
  - Uses a "natural" pseudocode language similar to the one used in Algobox and school books.
  - Assisted development
- Program mode
  - Uses Python, for the more experienced

In both modes, the code can be debugged and executed step-by-step to facilitate the problem-solving side of development.

## Using Turing

Turing is cross-platform, but has only been tested on Windows and Linux-based operating systems. macOS should be supported, but no guarantee is made of that.

### Using the package (recommended for Linux)

A package is available for Ubuntu and Debian. You can install it like this:

`sudo apt-get install turing`

If it does not work, use the pre-compiled binaries available below.

### Using pre-compiled binaries (recommended)

Click on the [**Releases**](https://github.com/TuringApp/Turing/releases) tab at the top of the page and download the release corresponding to your OS.

- `windows32`: Windows 32 bits (7 or later)
	- tested on 10 x64
- `nix64`: Linux 64 bits (Ubuntu 14.04 / Debian 8 or later) 
	- tested on 18.04
- `osx`: macOS 64 bits (10.13 *High Sierra* or later)
	- tested on 10.13

### Using the source code (advanced users)

#### Python 3.6 required!

**You need to have `python3` point to Python 3.6 in your shell! Either use an alias in your `.bashrc` or a distribution that comes with Python 3.6.**

It uses the following libraries:

- [PyQt 5](https://riverbankcomputing.com/software/pyqt/) - UI framework
- [pyQode](https://github.com/pyQode/pyQode) - PyQt code editor with syntax highlighting
- [Pygments](http://pygments.org/) - Syntax highlighter for printing code files
- [pep8](https://pypi.python.org/pypi/pep8) - Code quality checker

First, install everything using pip:

    pip install --ignore-installed -r requirements.txt

Note: if you have Python 2.x installed on your computer (which is the case on 99% of Linux distributions), the old `pip` may be present in `PATH` and interfere with the above command line. If that happens, try using `pip3` instead of `pip`. Of course, it must be the `pip` paired with the installed Python3 (so you may need to use `pip3.6` instead).

Next, open the src/ folder and use `run.bat` or `source run.sh` depending on your operating system.

#### Building Turing (using pyInstaller)

You need:

- Python 3.6 (`python3.6`)
- Python 3.6 dev package (`python3.6-dev`)
- Qt5 `lrelease` (`qt5-dev-tools`)

## Contributing

We're currently looking for translators. For more information, see the [CONTRIBUTING.md](CONTRIBUTING.md) file and [the Gitter](https://gitter.im/TuringDevelopment).

If you're a developer and you found a bug somewhere and fixed it, feel free to make a PR, we usually answer in no more than a few hours.

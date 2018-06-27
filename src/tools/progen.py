# -*- coding: utf-8 -*-

import glob

files = glob.iglob('../**/*.py', recursive=True)

with open("../project.pro", "w") as file:
    file.write(r"""

CODECFORTR = UTF-8
CODECFORSRC = UTF-8

""")

    file.write(r"""RESOURCES += \
    turing.qrc

SOURCES += \
""")
    file.write(" \\\n".join("    " + x[3:] for x in glob.iglob('../**/*.py', recursive=True) if "pycache" not in x))

    file.write(r"""
    
FORMS += \
""")

    file.write(" \\\n".join("    " + x[3:] for x in glob.iglob('../**/*.ui', recursive=True)))

    file.write(r"""
    
TRANSLATIONS += \
""")

    file.write(" \\\n".join("    " + x[3:] for x in glob.iglob('../**/*.ts', recursive=True)))


for ts in glob.iglob('../**/*.ts', recursive=True):
    with open(ts, "r", encoding="utf8") as f:
        orig = f.read()
    orig = orig.replace('<message>', '<message encoding="UTF-8">')
    with open(ts, "w", encoding="utf8") as f:
        f.write(orig)


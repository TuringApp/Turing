# -*- coding: utf-8 -*-

import glob

files = glob.iglob('../**/*.py', recursive=True)

with open("../project.pro", "w") as file:
    file.write(r"""RESOURCES += \
    turing.qrc

SOURCES += \
""")
    file.write(" \\\n".join("    " + x[3:] for x in glob.iglob('../**/*.py', recursive=True)))

    file.write(r"""
    
FORMS += \
""")

    file.write(" \\\n".join("    " + x[3:] for x in glob.iglob('../**/*.ui', recursive=True)))

    file.write(r"""
    
TRANSLATIONS += \
""")

    file.write(" \\\n".join("    " + x[3:] for x in glob.iglob('../**/*.ts', recursive=True)))

# -*- coding: utf-8 -*-

import json
import os
import sys

## add a path to get the embedded unmaintained package pyqode
sys.path.insert(0,
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
import threading

from PyQt5.QtCore import QSettings, QCoreApplication, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QStyleFactory, QSplashScreen

import util
from util import theming, show_error


translate = QCoreApplication.translate

util.__version__ = "β-0.11"
util.__channel__ = "beta"


def except_hook(type, value, tback):
    show_error()

    sys.__excepthook__(type, value, tback)


def setup_thread_excepthook():
    """
    Workaround for `sys.excepthook` thread bug from:
    http://bugs.python.org/issue1230540

    Call once from the main thread before creating any threads.
    """

    init_original = threading.Thread.__init__

    def init(self, *args, **kwargs):

        init_original(self, *args, **kwargs)
        run_original = self.run

        def run_with_except_hook(*args2, **kwargs2):
            try:
                run_original(*args2, **kwargs2)
            except Exception:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


if __name__ == "__main__":
    sys.excepthook = except_hook
    setup_thread_excepthook()

    theming.app = app = QApplication(sys.argv)
    app.setApplicationName("Turing")
    app.setApplicationVersion(util.__version__)

    util.settings = QSettings("Turing", "Turing")
    ## check the format of "recent"'s value
    try:
        recent = json.loads(util.settings.value("recent", "[]"))
        assert (type(recent) is list)
        ## as of 2018-06-03, There was a bug with QSettings, which
        ## could not deal with empty lists: such a data was stored
        ## as @Invalid() and restored as None, which is not an empty list.
        ## so the format will be a string, serialized with JSON which
        ## is less buggy, and provides a well readable conffile.
    except:
        ## so, if some old-fashioned data were in the conffile,
        ## just forget it.
        util.settings.setValue("recent", json.dumps([]))
    util.translate_backend = translate

    DEFAULT_STYLE = QStyleFactory.create(app.style().objectName())

    if sys.platform == "win32":
        # fix for ugly font on 7+
        font = QFont("Segoe UI", 9)
        app.setFont(font)

    # noinspection PyUnresolvedReferences
    import turing_rc

    splash = QSplashScreen(QPixmap(":/icon/media/icon_128.png"), Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    try:
        theming.themes["custom"] = (theming.themes["custom"][0], util.settings.value("custom_theme", [], type=list))
    except:
        pass

    from forms import mainwindow

    mainwindow.init_main(splash)

    try:
        exitCode = app.exec_()
    except:
        show_error()
        exitCode = 1

    mainwindow.clean_exit()

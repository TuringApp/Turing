# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_calculator import Ui_CalcWindow
from maths.parser import Parser
from maths.evaluator import Evaluator
from util.math import properstr

def addResult(expr, result, error = False):
	if expr:
		i1 = QListWidgetItem()
		txt = str(expr)
		i1.setText(txt)
		i1.setToolTip(txt)
		ui.lstHistory.addItem(i1)

	i2 = QListWidgetItem()
	txt = properstr(result)
	i2.setText(txt)
	i2.setTextAlignment(Qt.AlignRight)
	if error:
		i2.setForeground(QBrush(QColor("red")))
	else:
		i2.setToolTip(txt)
	ui.lstHistory.addItem(i2)	

def calc():
	ev = Evaluator()
	expr = ui.txtExpr.text()
	ret = ev.evaluate(expr)
	msgs = ev.log.getMessages()	
	if msgs:
		err = "\n".join([x[1] for x in msgs])
		addResult(ev.beautified, err, True)
	if ret != None:
		addResult(None if msgs else ev.beautified, ret)
	else:
		addResult(None if msgs else ev.beautified, "Result is None", True)

def dclick(item):
	if item.toolTip():
		ui.txtExpr.setText(item.text()) 

def initUi():
    global window, ui
    window = QMainWindow()
    ui = Ui_CalcWindow()
    ui.setupUi(window)
    ui.btnCalc.clicked.connect(calc)
    ui.lstHistory.itemDoubleClicked.connect(dclick)
    window.show()

def run():
	initUi()
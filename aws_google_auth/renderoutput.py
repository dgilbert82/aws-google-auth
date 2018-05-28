#!/usr/bin/python

import sys
import getpass
# Import PySide classes
from PySide.QtCore import *
from PySide.QtGui import *


class Surface:
    def __init__(self, surfacetype):
        '''
        Create an output surface.  Supported types are console or gui
        where gui is a pyside (Qt) gui.
        '''

        self.surfacetype = surfacetype
        if QApplication.instance() is not None:
            self.app = QApplication.instance()
        else:
            self.app = QApplication(sys.argv)
            
        self.win = QWidget()
        self.msgBox = QMessageBox()
        self.dialog = QLineEdit()
        self.form = QFormLayout()
        self.button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        self.form.addRow("Input:", self.dialog)
        self.form.addWidget(self.button)
        
        self.win.resize(600, 100)
        self.win.setLayout(self.form)
         
        # Place it at the bottom right, narrower than
        # the other interactive widgets
        self.button.setMinimumWidth(145)
        self.button.move(445, 50)


    def displayMessage(self, message):
        if self.surfacetype == 'console':
            print("rendered output is: {}".format(message))
        elif self.surfacetype == 'gui':
            self.msgBox.setText(message)
            self.msgBox.show()
            self.app.exec_()


    def getInput(self, prompt):
        if self.surfacetype == 'console':
            return input(prompt)
        elif self.surfacetype == 'gui':
            self.win.setWindowTitle(prompt)
            self.win.show()
            self.app.exec_()
            return self.dialog.text()


    def getPass(self, prompt):
        if self.surfacetype == 'console':
            return getpass.getpass(prompt)
        elif self.surfacetype == 'gui':
            self.win.setWindowTitle(prompt)
            self.dialog.setEchoMode(QLineEdit.Password)
            self.button.rejected.connect(self.app.exit)
            #self.button.accepted.connect(pass)
            self.button.show()
            self.win.show()
            self.app.exec_()
            return self.dialog.text()

import sys

from PyQt5.QtWidgets import (QWidget, QMainWindow,  
    QAction, QApplication, QLabel, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem,QLineEdit, QTableWidget)
    #, QComboBox, QPushButton, QCheckBox)

from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtGui import QIcon
#from PyQt5.QtCore import *

class centralWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox_top = QHBoxLayout() 
        hbox_top.addWidget(QLineEdit()) 
        hbox = QHBoxLayout()
        hbox.addWidget(QTableWidget())
        # just for show
        hbox.addWidget(QLabel('test'))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_top)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
         

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):      

        self.mainWidget = centralWidget()
        self.setCentralWidget(self.mainWidget)
        self.statusBar()

        #setup actions for the menu
        #openFile = QAction(QIcon('open.png'), 'Open', self)
        #openFile.setShortcut('Ctrl+O')
        #openFile.setStatusTip('Open new File')
        #openFile.triggered.connect(self.showDialog)
        closeApp = QAction(QIcon('close.png'), 'Exit', self)
        closeApp.setShortcut('Esc')
        closeApp.setStatusTip('Close the application')
        closeApp.triggered.connect(self.close)

        # create the menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(openFile)       
        fileMenu.addAction(closeApp)       
        
        # basic geometry/params
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('QtDAWN')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())



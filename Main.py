import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import*
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from OCC.Core import V3d
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import random
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
from Primitives import *
from Dock import *
from OCC.Display.backend import load_backend, load_pyqt5, PYQT5
load_backend(PYQT5)
load_pyqt5()
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Core.Aspect import Aspect_GDM_Lines, Aspect_GT_Rectangular
from OCC.Core.AIS import AIS_Shaded, AIS_Shape, AIS_WireFrame
from OCC.Core.Aspect import Aspect_TOTP_RIGHT_LOWER

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.x, self.y, self.z = self.createFormGroupBox()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
                
    def createFormGroupBox(self):
        x = QLineEdit()
        #y = QSpinBox()
        y = QSpinBox()
        z = QLineEdit()
        self.formGroupBox = QGroupBox("Input")
        layout = QFormLayout()
        
        layout.addRow(QLabel("x coordinate:"), x)
        layout.addRow(QLabel("y coordinate:"), y)
        layout.addRow(QLabel("z coordinate:"), z)
        self.formGroupBox.setLayout(layout)
        return x,y,z
    
class Input(QWidget):
        def __init__(self):
            super().__init__()

        def getInteger(self, title, shape_name, coordinate, minimum=0):
            i, okPressed = QInputDialog.getInt(self, title, coordinate + " :", 0, minimum, 100, 1)
            #Parameters in order: self, window title, label (before input box), default value, minimum, maximum and step size.
            if okPressed:
                print(i)

        def getDouble(self, title, shape_name, coordinate):
            d, okPressed = QInputDialog.getDouble(self, title, coordinate + " :", 00.00, 0, 100, 5)
            #The last parameter (5) is the number of decimals behind the comma.
            if okPressed:
                return d

        def getChoice(self):
            items = ("Red","Blue","Green")
            item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
            if okPressed and item:
                print(item)

        def getText(self):
            text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
            if okPressed and text != '':
                print(text)
        
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.input = Input()
        self.form = Dialog()
        self.list = QListWidget()
        self.dock1 = DockDialog(self)
        self.canva = qtViewer3d(self)
        
        self._splitter1 = QSplitter(Qt.Vertical)
        self._splitter1.addWidget(self.canva)
        self._splitter = QSplitter(Qt.Horizontal)
        self._splitter.addWidget(self.dock1)
        self._splitter.addWidget(self._splitter1)
        self.setCentralWidget(self._splitter1)
        
        self.title = '3D Modelling'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
    def main(self):
        
        exit = QtWidgets.QAction("&Exit the system", self)
        exit.setShortcut("Ctrl+X")
        exit.setStatusTip('Leave The App')
        exit.triggered.connect(self.exit)
               
        open_file = QtWidgets.QAction("&Open a File", self)
        open_file.setShortcut("Ctrl+O")
        #open_file.triggered.connect(self.open)
        
        dock = QtWidgets.QAction("&Dock", self)
        dock.triggered.connect(_Dock)
        
        form = QtWidgets.QAction("&Form", self)
        form.triggered.connect(_Form)
        
        fitall = QtWidgets.QAction("&Fit All", self)
        form.triggered.connect(_FitAll)
        
        circle = QtWidgets.QAction("&Disk", self)
        circle.triggered.connect(_Disk)
        
        triangle = QtWidgets.QAction("&Triangle", self)
        triangle.triggered.connect(_Triangle)
        
        rectangle = QtWidgets.QAction("&Rectangle", self)
        rectangle.triggered.connect(_Rectangle)
        
        polygon = QtWidgets.QAction("&Polygon", self)
        polygon.triggered.connect(_Polygon)

        #Main Menu
        main_menu = self.menuBar()

        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(open_file)
        bool_menu = main_menu.addMenu('&Draw')
        bool_menu.addAction(circle)
        bool_menu.addAction(triangle)
        bool_menu.addAction(rectangle)
        bool_menu.addAction(polygon)
        view_menu = main_menu.addMenu('&View')
        view_menu.addAction(dock)
        view_menu.addAction(form)
        view_menu.addAction(fitall)
        exit_menu = main_menu.addMenu('&Exit')
        exit_menu.addAction(exit)
        self.statusBar()
        
    def exit(self):
        sys.exit(1)

def _Form():
    ex1._splitter1.addWidget(ex1.form)
    ex1.form.__init__()    
    
def _Dock():
    ex1.dock1.__init__(ex1)
    
def _FitAll():
    ex1.canva._display.FitAll()
        
def _Disk():
    disk = Primitives.Disk(display, ex1)
    ex1.dock1.addItem(ex1, disk, "Disk")

def _Triangle():
    triangle = Primitives.Triangle(display, ex1)
    ex1.dock1.addItem(ex1, triangle, "Triangle")
    
def _Rectangle():
    rectangle = Primitives.Rectangle(display, ex1)
    ex1.dock1.addItem(ex1, rectangle, "Rectangle")
    
def _Polygon():
    polygon = Primitives.Polygon(display, ex1)
    ex1.dock1.addItem(ex1, polygon, "Polygon")
        
def Main():
    app = QApplication(sys.argv)
    ex1 = MainWindow()
    
    ex1.canva.InitDriver()
    ex1.canva.qApp = app
    display = ex1.canva._display
    context = display.GetContext()
    view = display.GetView()
    viewer = display.GetViewer()
    viewer.ActivateGrid(Aspect_GT_Rectangular,Aspect_GDM_Lines)
    view.SetBackgroundColor(Quantity_Color(1, 1, 1, 0))
    context.SetDisplayMode(AIS_Shaded,True)
    #view.TriedronDisplay(Aspect_TOTP_RIGHT_LOWER, Quantity_Color(Quantity_NOC_BLACK), 0.08, V3d.V3d_WIREFRAME)
    # can be replaced by with little difference.
    display.display_triedron()
    
    Primitives.Cube(display)
    ex1.main()
    ex1.show()
    sys.exit(app.exec_())
    
Main()
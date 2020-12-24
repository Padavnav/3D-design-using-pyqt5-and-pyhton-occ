from PyQt5.QtWidgets import *
from PyQt5.QtCore import*

class DockDialog(QMainWindow):
    def __init__(self,parents):
        super().__init__()
        
        parents.dock = QDockWidget("SHAPES", parents)
        parents.addDockWidget(Qt.LeftDockWidgetArea, parents.dock)
        
        parents.dock.setWidget(parents.list)
        
    def addItem(self, parents, shape, shape_name):
        parents.list.addItem(shape_name)
        #parents.list.itemDoubleClicked.connect(shape)

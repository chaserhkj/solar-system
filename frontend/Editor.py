#!/usr/bin/env python2
import PyQt4.QtCore as c
import PyQt4.QtGui as g
import IO

class Editor(g.QWidget):
    dataUpdated = c.pyqtSignal()
    def openFile(self):
        filename = g.QFileDialog.getOpenFileName(self)
        if filename:
            self._io.load(filename)
            self.dataUpdated.emit()
        
    def saveFile(self):
        filename = g.QFileDialog.getSaveFileName(self)
        self._io.save(filename)

    def updateDisplayedData(self):
        pass
        
    def __init__(self,parent=None):
        g.QWidget.__init__(self, parent)

        self._io = IO.EdittimeIO()
        
        self._layout = g.QVBoxLayout()

        layout = g.QHBoxLayout()
        openB = g.QPushButton("Open")
        saveB = g.QPushButton("Save")
        layout.addWidget(openB)
        layout.addWidget(saveB)
        self._layout.addLayout(layout)
        openB.clicked.connect(self.openFile)
        saveB.clicked.connect(self.saveFile)
        
        self._layout.addWidget(g.QLabel("<b>Global settings</b>"))

        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Calculation step"))
        self._step = g.QLineEdit()
        layout.addWidget(self._step)
        layout.addWidget(g.QLabel("Gravity constant"))
        self._g = g.QLineEdit()
        layout.addWidget(self._g)
        layout.addWidget(g.QLabel("Initial time"))
        self._t = g.QLineEdit()
        layout.addWidget(self._t)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Recursion depth"))
        self._r = g.QLineEdit()
        layout.addWidget(self._r)
        layout.addWidget(g.QLabel("Recursive coefficient"))
        self._o = g.QLineEdit()
        layout.addWidget(self._o)
        layout.addWidget(g.QLabel("Thread count"))
        self._numt = g.QLineEdit()
        layout.addWidget(self._numt)
        self._aplfx = g.QCheckBox("Fix applied")
        layout.addWidget(self._aplfx)
        self._layout.addLayout(layout)

        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Drawing scale"))
        self._scale = g.QLineEdit()
        layout.addWidget(self._scale)
        layout.addWidget(g.QLabel("Step per frame"))
        self._step_count = g.QLineEdit()
        layout.addWidget(self._step_count)
        layout.addWidget(g.QLabel("Frame interval"))
        self._interval = g.QLineEdit()
        layout.addWidget(self._interval)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Plane scale"))
        self._plane_scale = g.QLineEdit()
        layout.addWidget(self._plane_scale)
        layout.addWidget(g.QLabel("Plane cell density"))
        self._cell_density = g.QLineEdit()
        layout.addWidget(self._cell_density)
        button = g.QPushButton("Set plane color")
        self._plane_color = g.QColor(255,255,255)
        def setPlaneColor():
            self._plane_color = g.QColorDialog\
                                 .getColor(self._plane_color)
        button.clicked.connect(setPlaneColor)
        layout.addWidget(button)
        self._layout.addLayout(layout)
        
        self._listWidget = g.QListWidget()
        self._layout.addWidget(self._listWidget)

        self._name = g.QLineEdit()
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Name (optional)"))
        layout.addWidget(self._name)
        self._mass = g.QLineEdit()
        layout.addWidget(g.QLabel("Mass"))
        layout.addWidget(self._mass)
        self._layout.addLayout(layout)
        
        self._px = g.QLineEdit()
        self._py = g.QLineEdit()
        self._pz = g.QLineEdit()
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("X"))
        layout.addWidget(self._px)
        layout.addWidget(g.QLabel("Y"))
        layout.addWidget(self._py)
        layout.addWidget(g.QLabel("Z"))
        layout.addWidget(self._pz)
        self._layout.addLayout(layout)
        
        self._vx = g.QLineEdit()
        self._vy = g.QLineEdit()
        self._vz = g.QLineEdit()
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Vx"))
        layout.addWidget(self._vx)
        layout.addWidget(g.QLabel("Vy"))
        layout.addWidget(self._vy)
        layout.addWidget(g.QLabel("Vz"))
        layout.addWidget(self._vz)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        updateB = g.QPushButton("Update")
        addB = g.QPushButton("Add")
        delB = g.QPushButton("Delete")
        layout.addWidget(updateB)
        layout.addWidget(addB)
        layout.addWidget(delB)
        self._layout.addLayout(layout)
        
        self.setWindowTitle("Cela System Editor")
        self.setLayout(self._layout)
        self.resize(600,600)
a=Editor()
a.show()        

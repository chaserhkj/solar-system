#!/usr/bin/env python2
# import PyQt4.QtCore as c
import PyQt4.QtGui as g
import IO

class Editor(g.QWidget):
    def saveFile(self):
        
    def __init__(self,parent=None):
        g.QWidget.__init__(self, parent)

        self._io = IO.EdittimeIO()
        
        self._layout = g.QVBoxLayout()

        self._a_layout = g.QHBoxLayout()
        openB = g.QPushButton("Open")
        saveB = g.QPushButton("Save")
        self._a_layout.addWidget(openB)
        self._a_layout.addWidget(saveB)
        self._layout.addLayout(self._a_layout)
        openB.clicked.connect(self.saveFile)
        
        
        self._listWidget = g.QListWidget()
        self._layout.addWidget(self._listWidget)

        name = g.QLabel("Name (optional)")
        self._name = g.QLineEdit()
        n_layout = g.QHBoxLayout()
        n_layout.addWidget(name)
        n_layout.addWidget(self._name)
        self._layout.addLayout(n_layout)
        
        mass = g.QLabel("Mass")
        self._mass = g.QLineEdit()
        m_layout = g.QHBoxLayout()
        m_layout.addWidget(mass)
        m_layout.addWidget(self._mass)
        self._layout.addLayout(m_layout)
        
        px = g.QLabel("X")
        py = g.QLabel("Y")
        pz = g.QLabel("Z")
        self._px = g.QLineEdit()
        self._py = g.QLineEdit()
        self._pz = g.QLineEdit()
        p_layout = g.QHBoxLayout()
        p_layout.addWidget(px)
        p_layout.addWidget(self._px)
        p_layout.addWidget(py)
        p_layout.addWidget(self._py)
        p_layout.addWidget(pz)
        p_layout.addWidget(self._pz)
        self._layout.addLayout(p_layout)
        
        vx = g.QLabel("Vx")
        vy = g.QLabel("Vy")
        vz = g.QLabel("Vz")
        self._vx = g.QLineEdit()
        self._vy = g.QLineEdit()
        self._vz = g.QLineEdit()
        v_layout = g.QHBoxLayout()
        v_layout.addWidget(vx)
        v_layout.addWidget(self._vx)
        v_layout.addWidget(vy)
        v_layout.addWidget(self._vy)
        v_layout.addWidget(vz)
        v_layout.addWidget(self._vz)
        self._layout.addLayout(v_layout)
        
        act_layout = g.QHBoxLayout()
        updateB = g.QPushButton("Update")
        addB = g.QPushButton("Add")
        delB = g.QPushButton("Delete")
        act_layout.addWidget(updateB)
        act_layout.addWidget(addB)
        act_layout.addWidget(delB)
        self._layout.addLayout(act_layout)
        
        self.setWindowTitle("Cela System Editor")
        self.setLayout(self._layout)

# from PyQt4.QtGui import QApplication
# app = QApplication([])

e=Editor()
e.show()        

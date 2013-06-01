#!/usr/bin/env python2
import PyQt4.QtCore as c
import PyQt4.QtGui as g
import IO
import sys

def _setv(dic, key, dest, mod=None):
    try:
        if mod != None:
            dest(mod(dic[key]))
        else:
            dest(dic[key])
    except KeyError:
        pass

def _color(rgb):
    return int(rgb[2]*255 + rgb[1]*255*256 + rgb[0]*255*256**2)


def _style(string):
    if string == "solid":
        return 1
    else:
        return 0

def _getv(dic, key, res, mod=None, assign=False):
    if mod != None:
        if assign:
            dic[key] = mod(res)
        else:
            dic[key] = mod(res())
    else:
        if assign:
            dic[key] = res
        else:
            dic[key] = res()
        
def _color_r(color):
    return [color.red()/255.0,color.green()/255.0,color.blue()/255.0]

def _style_r(value):
    if value == 1:
        return "solid"
    else:
        return "wired"
        
class DoubleValidator(g.QValidator):
    def __init__(self, default, bot, top, dec, parent=None):
        g.QValidator.__init__(self, parent)
        self._validator = g.QDoubleValidator(bot, top, dec, self)
        self._default = default

    def validate(self, inputs ,pos):
        return self._validator.validate(inputs, pos)
        
    def fixup(self, inputs):
        inputs.swap(self._default)

class IntValidator(g.QValidator):
    def __init__(self, default, bot, top,  parent=None):
        g.QValidator.__init__(self, parent)
        self._validator = g.QIntValidator(bot, top, self)
        self._default = default

    def validate(self, inputs ,pos):
        return self._validator.validate(inputs, pos)
        
    def fixup(self, inputs):
        inputs.swap(self._default)

class Editor(g.QWidget):
    dataUpdated = c.pyqtSignal()
    def openFile(self):
        filename = g.QFileDialog.getOpenFileName(self)
        if filename:
            try:
                self._io.load(filename)
            except Exception as e:
                g.QMessageBox.critical(self, "I/O error","Load exception %s: %s"%(e.__class__.__name__, e))
            self.dataUpdated.emit()
        
    def saveFile(self):
        self.saveDisplayedData()
        filename = g.QFileDialog.getSaveFileName(self)
        if filename:
            try:
                self._io.save(filename)
            except Exception as e:
                g.QMessageBox.critical(self, "I/O error","Save exception %s: %s"%(e.__class__.__name__, e))



    def saveDisplayedData(self):
        _getv(self._io.data["global"],"Calculation step",self._step.text, float)
        _getv(self._io.data["global"],"Gravity constant",self._g.text, float)
        _getv(self._io.data["global"],"Initial time",self._t.text, float)
        _getv(self._io.data["global"],"Recursion depth",self._r.text, int)
        _getv(self._io.data["global"],"Recursive coefficient",self._o.text, float)
        _getv(self._io.data["global"],"Thread count",self._numt.text, int)
        _getv(self._io.data["global"],"Drawing scale",self._scale.text, float)
        _getv(self._io.data["global"],"Step per frame",self._step_count.text, int)
        _getv(self._io.data["global"],"Frame interval",self._interval.text, int)
        _getv(self._io.data["global"],"Plane scale",self._plane_scale.text, float)
        _getv(self._io.data["global"],"Plane cell density",self._cell_density.text, int)
        _getv(self._io.data["global"],"Trace buffer size",self._trace_buffer_size.text, int)
        _getv(self._io.data["global"],"Axis length",self._axis_length.text, int)
        _getv(self._io.data["global"],"Line width",self._line_width.text, float)
        _getv(self._io.data["global"],"Line drawing interval",self._line_drawing_interval.text, int)
        _getv(self._io.data["global"],"Plane color",self._plane_color, _color_r, True)
        _getv(self._io.data["global"],"Axis color",self._axis_color, _color_r, True)
        _getv(self._io.data["global"],"Fix applied",self._aplfx.isChecked, bool)
        _getv(self._io.data["global"],"Show shadow line",self._show_shadow_line.isChecked, bool)
        _getv(self._io.data["global"],"Enable lighting",self._enable_lighting.isChecked, bool)
        _getv(self._io.data["global"],"Enable multi-sampling",self._enable_multi_sampling.isChecked, bool)
        _getv(self._io.data["global"],"Enable smooth",self._smooth.currentIndex, int)
        _getv(self._io.data["global"],"Default sphere style",self._default_style.currentIndex, _style_r)
        
        
    def updateDisplayedData(self):
        _setv(self._io.data["global"],"Calculation step",self._step.setText, str)
        _setv(self._io.data["global"],"Gravity constant",self._g.setText, str)
        _setv(self._io.data["global"],"Initial time",self._t.setText, str)
        _setv(self._io.data["global"],"Recursion depth",self._r.setText, str)
        _setv(self._io.data["global"],"Recursive coefficient",self._o.setText, str)
        _setv(self._io.data["global"],"Thread count",self._numt.setText, str)
        _setv(self._io.data["global"],"Drawing scale",self._scale.setText, str)
        _setv(self._io.data["global"],"Step per frame",self._step_count.setText, str)
        _setv(self._io.data["global"],"Frame interval",self._interval.setText, str)
        _setv(self._io.data["global"],"Plane scale",self._plane_scale.setText, str)
        _setv(self._io.data["global"],"Plane cell density",self._cell_density.setText, str)
        _setv(self._io.data["global"],"Trace buffer size",self._trace_buffer_size.setText, str)
        _setv(self._io.data["global"],"Axis length",self._axis_length.setText, str)
        _setv(self._io.data["global"],"Line width",self._line_width.setText, str)
        _setv(self._io.data["global"],"Line drawing interval",self._line_drawing_interval.setText, str)
        _setv(self._io.data["global"],"Plane color",self._plane_color.setRgb, _color)
        _setv(self._io.data["global"],"Axis color",self._axis_color.setRgb, _color)
        _setv(self._io.data["global"],"Fix applied",self._aplfx.setChecked, bool)
        _setv(self._io.data["global"],"Show shadow line",self._show_shadow_line.setChecked, bool)
        _setv(self._io.data["global"],"Enable lighting",self._enable_lighting.setChecked, bool)
        _setv(self._io.data["global"],"Enable multi-sampling",self._enable_multi_sampling.setChecked, bool)
        _setv(self._io.data["global"],"Enable smooth",self._smooth.setCurrentIndex, int)
        _setv(self._io.data["global"],"Default sphere style",self._default_style.setCurrentIndex, _style)
        self._treeWidget.clear()
        for i in xrange(len(self._io.data["celas"])):
            cela = self._io.data["celas"][i]
            item = g.QTreeWidgetItem(self._treeWidget)
            item.setText(0, str(i))
            item.setText(1, cela.get("name") or "")
            item.setText(2, str(cela["mass"]))
            item.setText(3, str(cela["radius"]))


    def _select_handle(self,current,previous):
        if current == None:
            self._name.setText("")
            self._mass.setText("")
            self._radius.setText("")
            self._px.setText("")
            self._py.setText("")
            self._pz.setText("")
            self._vx.setText("")
            self._vy.setText("")
            self._vz.setText("")
            self._graphic_radius.setText("")
            self._style.setCurrentIndex(self._default_style.currentIndex())
            self._graphic_color = g.QColor(153,204,255)
            return
        data = self._io.data["celas"][int(current.text(0))]
        _setv(data,"name",self._name.setText, str)
        _setv(data,"mass",self._mass.setText, str)
        _setv(data,"radius",self._radius.setText, str) 
        _setv(data["position"],0,self._px.setText, str)
        _setv(data["position"],1,self._py.setText, str)
        _setv(data["position"],2,self._pz.setText, str)
        _setv(data["velocity"],0,self._vx.setText, str)       
        _setv(data["velocity"],1,self._vy.setText, str)
        _setv(data["velocity"],2,self._vz.setText, str)
        _setv(data["graphic"],"radius",self._graphic_radius.setText, str)
        _setv(data["graphic"],"style",self._style.setCurrentIndex, _style)
        _setv(data["graphic"],"color",self._graphic_color.setRgb, _color)

    def _update_handle(self):
        item = self._treeWidget.currentItem()
        if item == None:
            return
        data = self._io.data["celas"][int(item.text(0))]
        _getv(data,"name",self._name.text, str)
        _getv(data,"mass",self._mass.text, float)
        _getv(data,"radius",self._radius.text ,float) 
        _getv(data["position"],0,self._px.text, float)       
        _getv(data["position"],1,self._py.text, float)
        _getv(data["position"],2,self._pz.text, float)
        _getv(data["velocity"],0,self._vx.text, float)       
        _getv(data["velocity"],1,self._vy.text, float)
        _getv(data["velocity"],2,self._vz.text, float)
        _getv(data["graphic"],"radius",self._graphic_radius.text, float)
        _getv(data["graphic"],"style",self._style.currentIndex, _style_r)
        _getv(data["graphic"],"color",self._graphic_color, _color_r, True)
        self.dataUpdated.emit()

    def _add_handle(self):
        self._io.data["celas"].append({"position":[0,0,0],
                                       "velocity":[0,0,0],
                                       "radius":1.0,
                                       "mass":1.0,
                                       "name":"",
                                       "graphic":{
                                           "radius":1.0,
                                           "style":self._default_style.currentIndex() and "solid" or "wired",
                                           "color":[1,1,1]
                                       }
                                   })
        self.dataUpdated.emit()

    def _del_handle(self):
        item = self._treeWidget.currentItem()
        if item == None:
            return
        del self._io.data["celas"][int(item.text(0))]
        self.dataUpdated.emit()        
        
    def setDefaults(self):
        self._step.setText("0.010")
        self._g.setText("1.0")
        self._t.setText("0")
        self._r.setText("0")
        self._o.setText("0")
        self._numt.setText("0")
        self._aplfx.setChecked(False)
        self._scale.setText("10000")
        self._step_count.setText("10")
        self._interval.setText("20")
        self._plane_scale.setText("12000")
        self._cell_density.setText("20")
        self._plane_color = g.QColor(153,204,255)
        self._trace_buffer_size.setText("1000")
        self._axis_length.setText("20")
        self._axis_color = g.QColor(255,255,255)
        self._line_width.setText("1")
        self._line_drawing_interval.setText("5")
        self._show_shadow_line.setChecked(False)
        self._enable_lighting.setChecked(True)
        self._enable_multi_sampling.setChecked(True)
        self._smooth.setCurrentIndex(2)
        self._default_style.setCurrentIndex(0)
        
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
        self._step.setValidator(DoubleValidator("0.010",1e-8,1e8,8))
        layout.addWidget(self._step)
        layout.addWidget(g.QLabel("Gravity constant"))
        self._g = g.QLineEdit()
        self._g.setValidator(DoubleValidator("1.0",-1e8,1e8,8))
        layout.addWidget(self._g)
        layout.addWidget(g.QLabel("Initial time"))
        self._t = g.QLineEdit()
        self._t.setValidator(DoubleValidator("1",1e-8,1e8,8))
        layout.addWidget(self._t)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Recursion depth"))
        self._r = g.QLineEdit()
        self._r.setValidator(IntValidator("0",0,1e5))
        layout.addWidget(self._r)
        layout.addWidget(g.QLabel("Recursive coefficient"))
        self._o = g.QLineEdit()
        self._o.setValidator(DoubleValidator("0",0,2,8))
        layout.addWidget(self._o)
        layout.addWidget(g.QLabel("Thread count"))
        self._numt = g.QLineEdit()
        self._numt.setValidator(IntValidator("0",0,1e3))
        layout.addWidget(self._numt)
        self._aplfx = g.QCheckBox("Fix applied")
        layout.addWidget(self._aplfx)
        self._layout.addLayout(layout)

        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Drawing scale"))
        self._scale = g.QLineEdit()
        self._scale.setValidator(DoubleValidator("10000",1e-8,1e8,8))
        layout.addWidget(self._scale)
        layout.addWidget(g.QLabel("Step per frame"))
        self._step_count = g.QLineEdit()
        self._step_count.setValidator(IntValidator("10",1,1e8))
        layout.addWidget(self._step_count)
        layout.addWidget(g.QLabel("Frame interval"))
        self._interval = g.QLineEdit()
        self._interval.setValidator(IntValidator("20",1,1e8))
        layout.addWidget(self._interval)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Plane scale"))
        self._plane_scale = g.QLineEdit()
        self._plane_scale.setValidator(DoubleValidator("12000",1e-8,1e8,8))
        layout.addWidget(self._plane_scale)
        layout.addWidget(g.QLabel("Plane cell density"))
        self._cell_density = g.QLineEdit()
        self._cell_density.setValidator(IntValidator("20",1,1e8))
        layout.addWidget(self._cell_density)
        button = g.QPushButton("Set plane color")
        self._plane_color = g.QColor()
        def setPlaneColor():
            color = g.QColorDialog(self._plane_color, self)
            if color.exec_():
                self._plane_color = color.selectedColor()
        button.clicked.connect(setPlaneColor)
        layout.addWidget(button)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Trace buffer size"))
        self._trace_buffer_size = g.QLineEdit()
        self._trace_buffer_size.setValidator(IntValidator("1000",0,1e8))
        layout.addWidget(self._trace_buffer_size)
        layout.addWidget(g.QLabel("Axis length"))
        self._axis_length = g.QLineEdit()
        self._axis_length.setValidator(IntValidator("20",0,1e8))
        layout.addWidget(self._axis_length)
        button = g.QPushButton("Set Axis color")
        self._axis_color = g.QColor()
        def setAxisColor():
            color = g.QColorDialog(self._axis_color, self)
            if color.exec_():
                self._axis_color = color.selectedColor()
        button.clicked.connect(setAxisColor)
        layout.addWidget(button)
        self._layout.addLayout(layout)

        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Line width"))
        self._line_width = g.QLineEdit()
        self._line_width.setValidator(DoubleValidator("1",1e-8,1e8,8))
        layout.addWidget(self._line_width)
        layout.addWidget(g.QLabel("Line drawing interval"))
        self._line_drawing_interval = g.QLineEdit()
        self._line_drawing_interval.setValidator(IntValidator("5",1,1e8))
        layout.addWidget(self._line_drawing_interval)
        self._show_shadow_line = g.QCheckBox("Show shadow line")
        layout.addWidget(self._show_shadow_line)
        self._layout.addLayout(layout)

        layout = g.QHBoxLayout()
        self._layout.addLayout(layout)

        self._treeWidget = g.QTreeWidget()
        self._treeWidget.setHeaderLabels(["ID","Name","Mass","Radius"])
        self._treeWidget.currentItemChanged.connect(self._select_handle)
        self._enable_lighting = g.QCheckBox("Lighting")
        layout.addWidget(self._enable_lighting)
        self._enable_multi_sampling = g.QCheckBox("Multi-sampling")
        layout.addWidget(self._enable_multi_sampling)
        layout.addWidget(g.QLabel("Smooth"))
        self._smooth = g.QComboBox()
        self._smooth.insertItems(0,["Off", "Normal", "Best"])
        layout.addWidget(self._smooth)
        layout.addWidget(g.QLabel("Default sphere style"))
        self._default_style = g.QComboBox()
        self._default_style.insertItems(0,["Wired", "Solid"])
        layout.addWidget(self._default_style)
        self._layout.addWidget(self._treeWidget)

        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Name (optional)"))
        self._name = g.QLineEdit()
        layout.addWidget(self._name)
        layout.addWidget(g.QLabel("Mass"))
        self._mass = g.QLineEdit()
        self._mass.setValidator(DoubleValidator("1",-1e8,1e8,8))
        layout.addWidget(self._mass)
        layout.addWidget(g.QLabel("Radius"))
        self._radius = g.QLineEdit()
        self._radius.setValidator(DoubleValidator("1",1e-8,1e8,8))
        layout.addWidget(self._radius)
        self._layout.addLayout(layout)
        
        self._px = g.QLineEdit()
        self._py = g.QLineEdit()
        self._pz = g.QLineEdit()
        self._px.setValidator(DoubleValidator("0",-1e8,1e8,8))
        self._py.setValidator(DoubleValidator("0",-1e8,1e8,8))
        self._pz.setValidator(DoubleValidator("0",-1e8,1e8,8))
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
        self._vx.setValidator(DoubleValidator("0",-1e8,1e8,8))
        self._vy.setValidator(DoubleValidator("0",-1e8,1e8,8))
        self._vz.setValidator(DoubleValidator("0",-1e8,1e8,8))
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Vx"))
        layout.addWidget(self._vx)
        layout.addWidget(g.QLabel("Vy"))
        layout.addWidget(self._vy)
        layout.addWidget(g.QLabel("Vz"))
        layout.addWidget(self._vz)
        self._layout.addLayout(layout)
        
        layout = g.QHBoxLayout()
        layout.addWidget(g.QLabel("Graphical settings:"))
        layout.addWidget(g.QLabel("Radius"))
        self._graphic_radius = g.QLineEdit()
        self._graphic_radius.setValidator(DoubleValidator("1",1e-8,1e8,8))
        layout.addWidget(self._graphic_radius)
        layout.addWidget(g.QLabel("Style"))
        self._style = g.QComboBox()
        self._style.insertItems(0,["Wired", "Solid"])
        layout.addWidget(self._style)
        button = g.QPushButton("Set graphic color")
        self._graphic_color = g.QColor(153,204,255)
        def setGraphicColor():
            color = g.QColorDialog(self._graphic_color, self)
            if color.exec_():
                self._graphic_color = color.selectedColor()
        button.clicked.connect(setGraphicColor)
        layout.addWidget(button)
        self._layout.addLayout(layout)

        layout = g.QHBoxLayout()
        updateB = g.QPushButton("Update")
        addB = g.QPushButton("Add")
        delB = g.QPushButton("Delete")
        layout.addWidget(updateB)
        layout.addWidget(addB)
        layout.addWidget(delB)
        self._layout.addLayout(layout)
        
        self.setWindowTitle("System Editor")
        self.setLayout(self._layout)
        self.resize(600,600)
        self.setDefaults()

        self.dataUpdated.connect(self.updateDisplayedData)
        updateB.clicked.connect(self._update_handle)
        addB.clicked.connect(self._add_handle)
        delB.clicked.connect(self._del_handle)

if __name__ == '__main__':
    app = g.QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())

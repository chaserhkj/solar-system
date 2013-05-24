#!/usr/bin/env python2
import PyQt4.QtOpenGL as qgl
import PyQt4.QtCore as c
import PyQt4.QtGui as g
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import math
import galaxy

class ValueDisplayWidget(g.QWidget):
    def __init__(self, galaxy_obj, timer, trace ,parent=None):
        g.QWidget.__init__(self,parent)

        self._galaxy = galaxy_obj
        self._t = g.QLabel("")
        self._e = g.QLabel("")

        self._layout = g.QVBoxLayout()
        self._layout.addWidget(self._t)
        self._layout.addWidget(self._e)

        self._no = g.QLabel("")
        self._x = g.QLabel("")
        self._y = g.QLabel("")
        self._z = g.QLabel("")
        self._vx = g.QLabel("")
        self._vy = g.QLabel("")
        self._vz = g.QLabel("")
        self._layout.addWidget(self._no)
        self._layout.addWidget(self._x)
        self._layout.addWidget(self._y)
        self._layout.addWidget(self._z)
        self._layout.addWidget(self._vx)
        self._layout.addWidget(self._vy)
        self._layout.addWidget(self._vz)

        timer.timeout.connect(self.updateValue)
        
        self._trace = trace
        self.setLayout(self._layout)
        self.updateValue()

        self.setWindowTitle("Monitor")
        
    def setTrace(self, trace):
        self._trace = trace
        
    def updateValue(self):
        if self._trace == -1:
            self._no.setText("Tracing disabled.")
            self._x.setText("Object count: %s"%self._galaxy.getCelaNum())
            self._y.setText("Gravity constant: %s"%self._galaxy.getG())
            self._z.setText("Calculation step: %s"%self._galaxy.getStep())
            self._vx.setText("Recursive depth: %s"%self._galaxy.getRecDpt())
            self._vy.setText("Recursive coefficient: %s"%self._galaxy.getOmega())
            self._vz.setText("Fix applied: %s"%self._galaxy.appliedfix())
        else:
            array = galaxy.celaArray_frompointer(self._galaxy.output())
            if array[self._trace].name == "":
                name = "No. %s"%self._trace
            else:
                name = array[self._trace].name
            self._no.setText("Tracing object: %s"%name)
            self._x.setText("X: %s"%array[self._trace].p.x)
            self._y.setText("Y: %s"%array[self._trace].p.y)
            self._z.setText("Z: %s"%array[self._trace].p.z)
            self._vx.setText("Vx: %s"%array[self._trace].v.x)
            self._vy.setText("Vy: %s"%array[self._trace].v.y)
            self._vz.setText("Vz: %s"%array[self._trace].v.z)
        self._t.setText("Time: %s"%self._galaxy.getTime())
        self._e.setText("Energy: %s"%self._galaxy.getEnergy())
        
class DisplayWidget(qgl.QGLWidget):
    def __init__(self,
                 galaxy_obj,
                 graphic_obj,
                 scale,
                 step_count = 10,
                 interval = 20,
                 plane_scale = None,
                 plane_color = [0.6,0.8,1.0],
                 cell_density = 10,
                 parent = None):
        qgl.QGLWidget.__init__(self, parent)
        self.setWindowTitle("Display")
        self.resize(500,500)
        
        self._galaxy = galaxy_obj
        self._graphic = graphic_obj
        self._scale_factor = float(1)/float(scale)

        self._stepc = step_count
        self._interval = interval

        if plane_scale == None:
            self._planes = scale
        else:
            self._planes = plane_scale
            self._celld = cell_density
        self._planec = plane_color
        
        self._timer = c.QTimer(self)
        self._timer.timeout.connect(self.run)
        
        self._fs = False
        self._n = self._galaxy.getCelaNum()

        self._fs_sc = g.QShortcut("f",self)
        self._fs_sc.activated.connect(self.toggleFullScreen)

        self._exit_sc1 = g.QShortcut("q",self, self.close)
        self._exit_sc2 = g.QShortcut("Esc",self, self._esc_handler)

        self._zoomin_sc = g.QShortcut("=",self, self._zoomin)
        self._zoomout_sc = g.QShortcut("-",self, self._zoomout)

        self._upa_sc = g.QShortcut("Up", self, self._moveupa)
        self._downa_sc = g.QShortcut("Down", self, self._movedowna)
        self._lefta_sc = g.QShortcut("Left", self, self._movelefta)
        self._righta_sc = g.QShortcut("Right", self, self._moverighta)
        self._rin_sc = g.QShortcut("Ctrl+=",self, self._rin)
        self._rout_sc = g.QShortcut("Ctrl+-",self, self._rout)
        
        self._up_sc = g.QShortcut("w", self, self._moveup)
        self._down_sc = g.QShortcut("s", self, self._movedown)
        self._left_sc = g.QShortcut("a", self, self._moveleft)
        self._right_sc = g.QShortcut("d", self, self._moveright)
        
        self._inx_sc = g.QShortcut("y", self, self._inx)
        self._dex_sc = g.QShortcut("u", self, self._dex)
        self._iny_sc = g.QShortcut("h", self, self._iny)
        self._dey_sc = g.QShortcut("j", self, self._dey)
        self._inz_sc = g.QShortcut("n", self, self._inz)
        self._dez_sc = g.QShortcut("m", self, self._dez)

        self._trace_f_sc = g.QShortcut("t", self, self._trace_f)
        self._trace_b_sc = g.QShortcut("g", self, self._trace_b)
        self._trace_v_sc = g.QShortcut("b", self, self.toggleTraceV)
        
        self._reset_sc = g.QShortcut("/", self, self._reset_view)
        
        self._pause_sc = g.QShortcut("Space", self, self.togglePaused)
        
        self._trace = -1
        self._trace_v = False

        self._vDisplay = ValueDisplayWidget(self._galaxy, self._timer, self._trace,self)
        
        self._mouse_moving = -1
        
        self._reset()

    def _reset(self):
        
        self._view_angle = 30
        
        self._x = 0
        self._y = 0
        self._dx = 0
        self._dy = 0
        self._dz = 0
        self._rho = 3
        self._theta = 45
        self._phi = 45

    def _reset_view(self):
        self._reset()
        self._updateCamera()
        
    def _trace_f(self):
        self._trace = self._trace + 1
        if self._trace == self._n:
            self._trace = -1
        self._vDisplay.setTrace(self._trace)
        self.updateGL()
        self._vDisplay.updateValue()

    def _trace_b(self):
        self._trace = self._trace - 1
        if self._trace == -2:
            self._trace = self._n - 1
        self._vDisplay.setTrace(self._trace)
        self.updateGL()
        self._vDisplay.updateValue()
            
    def _inx(self):
        self._dx = self._dx + 0.05
        self._updateCamera()
        
    def _dex(self):
        self._dx = self._dx - 0.05
        self._updateCamera()
        
    def _iny(self):
        self._dy = self._dy + 0.05
        self._updateCamera()
        
    def _dey(self):
        self._dy = self._dy - 0.05
        self._updateCamera()

        
    def _inz(self):
        self._dz = self._dz + 0.05
        self._updateCamera()
        
    def _dez(self):
        self._dz = self._dz - 0.05
        self._updateCamera()
        
    def _esc_handler(self):
        if self._fs:
            self.toggleFullScreen()
        else:
            self.close()
            
    def _moveup(self):
        self._y = self._y - 0.05  
        self._updateCamera()

    def _movedown(self):
        self._y = self._y + 0.05
        self._updateCamera()

    def _moveleft(self):
        self._x = self._x + 0.05
        self._updateCamera()

    def _moveright(self):
        self._x = self._x - 0.05
        self._updateCamera()
        
    def _rin(self):
        self._rho = self._rho - 0.5
        self._updateCamera()

        
    def _rout(self):
        self._rho = self._rho + 0.5
        self._updateCamera()

    def _moveupa(self):
        self._theta = self._theta - 1
        self._updateCamera()

    def _movedowna(self):
        self._theta = self._theta + 1
        self._updateCamera()
        
    def _movelefta(self):
        self._phi = self._phi - 1
        self._updateCamera()

    def _moverighta(self):
        self._phi = self._phi + 1
        self._updateCamera()
            
    def _zoomin(self):
        self._view_angle = self._view_angle - 2
        self._updateCamera()
        
    def _zoomout(self):
        self._view_angle = self._view_angle + 2
        self._updateCamera()
        
    def run(self):
        for i in xrange(self._stepc):
            self._galaxy.run()
        self.updateGL()

    def _updateCamera(self):
        self.makeCurrent()
        self.setCamera()
        self.updateGL()

    def toggleTraceV(self):
        self._trace_v = not self._trace_v
        
    def toggleFullScreen(self):
        if self._fs:
            self.showNormal()
        else:
            self.showFullScreen()
        self._fs = not self._fs
            
    def start(self):
        self._timer.start(self._interval)

    def stop(self):
        self._timer.stop()

    def togglePaused(self):
        if self._timer.isActive():
            self.stop()
        else:
            self.start()

    def mousePressEvent(self,event):
        super(DisplayWidget, self).mousePressEvent(event)
        if event.button() == c.Qt.LeftButton:
            self._mouse_moving = 0
        elif event.button() == c.Qt.MidButton:
            self._mouse_moving = 1
        elif event.button() == c.Qt.RightButton:
            self._mouse_moving = 2
        self._mouse_x = event.x()
        self._mouse_y = event.y()
        event.accept()
        
    def mouseMoveEvent(self, event):
        super(DisplayWidget, self).mouseMoveEvent(event)
        if self._trace != -1 and self._trace_v:
            event.accept()
            return
        if self._mouse_moving == -1:
            event.accept()
            return
        elif self._mouse_moving == 0:
            self._phi = - (event.x() - self._mouse_x) / 10.0 + self._phi
            self._theta = - (event.y() - self._mouse_y) / 10.0 + self._theta
            self._updateCamera()
        elif self._mouse_moving == 2:
            self._x = (event.x() - self._mouse_x) / 800.0 + self._x
            self._y = - (event.y() - self._mouse_y) / 800.0 + self._y
            self._updateCamera()
        self._mouse_x = event.x()
        self._mouse_y = event.y()
        event.accept()
        
    def mouseReleaseEvent(self, event):
        super(DisplayWidget, self).mouseReleaseEvent(event)
        if self._mouse_moving == 1:
            self._reset_view()
        self._mouse_moving = -1
        event.accept()
        
    def wheelEvent(self,event):
        step = event.delta() / 100.0
        self._view_angle = self._view_angle - step
        self._updateCamera()
        event.accept()
        
    def _get_angle_by_v(self, v):
        phi = 180 + math.degrees(math.atan2(v.y , v.x))
        theta = 180 - math.degrees(math.atan2(math.sqrt(v.x**2 + v.y**2) ,v.z)) 
        return phi, theta

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        array = galaxy.\
                celaArray_frompointer(self._galaxy.\
                                      output())
        if self._trace >= 0:
            self._dx = array[self._trace].p.x * self._scale_factor
            self._dy = array[self._trace].p.y * self._scale_factor
            self._dz = array[self._trace].p.z * self._scale_factor
            if self._trace_v:
                self._phi, self._theta = self._get_angle_by_v(array[self._trace].v)
            self.setCamera()
        
        gl.glColor(*self._planec)
        step = self._planes / float(self._celld)
        for i in xrange(2 * self._celld):
            gl.glBegin(gl.GL_LINES)
            gl.glVertex(- self._planes + i*step,
                        - self._planes)
            gl.glVertex(- self._planes + i*step,
                        self._planes - step)
            gl.glEnd()
        for i in xrange(2 * self._celld):
            gl.glBegin(gl.GL_LINES)
            gl.glVertex(- self._planes,
                        - self._planes + i*step)
            gl.glVertex(self._planes - step,
                        - self._planes + i*step)
            gl.glEnd()

        for i in xrange(self._n):
            graphic = self._graphic[i]

            if "color" in graphic:
                gl.glColor(*graphic["color"])
            else:
                gl.glColor(*self._planec)

            if "type" in graphic and graphic["type"] == "solid":
                drawfunc = glut.glutSolidSphere
            else:
                drawfunc = glut.glutWireSphere
                
            gl.glPushMatrix()
            gl.glTranslate(array[i].p.x,
                           array[i].p.y,
                           array[i].p.z)
            drawfunc(graphic["radius"], 8, 8)
            gl.glPopMatrix()

    def setTraceCela(self,celaN):
        if celaN < -1 or celaN >= self._n :
            raise ValueError
        self._trace = celaN
        self._vDisplay.setTrace(celaN)

    def initializeGL(self):
        glut.glutInit([])
        gl.glClearColor(0,0,0,0)
        gl.glShadeModel(gl.GL_FLAT)

    def setCamera(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(self._view_angle, self._aspect, 0, 100)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslate(self._x, self._y, 0)
        glu.gluLookAt(self._rho * math.sin(math.radians(self._theta)) * math.cos(math.radians(self._phi)) + self._dx,
                      self._rho * math.sin(math.radians(self._theta)) * math.sin(math.radians(self._phi)) + self._dy,
                      self._rho * math.cos(math.radians(self._theta)) + self._dz,
                      self._dx, self._dy, self._dz,
                      0, 0, 1)
        gl.glScale(self._scale_factor,
                   self._scale_factor,
                   self._scale_factor)

        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        self._aspect = float(w)/float(h)
        self.setCamera()

        
